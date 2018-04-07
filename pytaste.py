#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
from psychopy import event, data, visual, core,logging

from utils import (check_if_file_exists, gen_paths, gen_concentration_steps,
                   get_start_val, get_exp_info, load_exp_info,
                   save_exp_info, get_bottle_index, gen_visual_stimuli,
                   find_nearest, plot)


exp_info_loaded = load_exp_info()
exp_info = get_exp_info(exp_info_loaded)

save_exp_info(exp_info)

path = gen_paths(exp_info)

if check_if_file_exists(path['csv_filename']):
    core.quit()

log_file = logging.LogFile(path['log_filename'], level=logging.EXP)
logging.console.setLevel(logging.WARNING)


win = visual.Window(fullscr=False, screen=0, allowGUI=True, color=[0, 0, 0])


min_trials = 10
previous_concentration = None
previous_detection_successful = False
concentration_steps = np.log10(gen_concentration_steps()[exp_info['Substance']])

start_val = np.log10(get_start_val(exp_info['Substance']))
quest_params = dict(startVal=start_val,
                    startValSd=np.log10(20),
                    pThreshold=0.82,
                    beta=3.5, gamma=0.01, delta=0.01, grain=0.01,
                    range=2*np.abs(concentration_steps.max()-concentration_steps.min()),
                    nTrials=20, stopInterval=None)

quest_handler = data.QuestHandler(**quest_params)
exp_handler = data.ExperimentHandler(extraInfo=exp_info,
                                     savePickle=True,
                                     saveWideText=True,
                                     dataFileName=os.path.join(
                                         path['rawdata_dir'],
                                         path['base_filename']))
exp_handler.addLoop(quest_handler)

vis_stimuli = gen_visual_stimuli(win)
msg = 'Did the participant recognize this concentration? [Y/N]'
vis_stimuli['detection_response'].setText(msg)

for concentration_proposed in quest_handler:
    trial_number = quest_handler.thisTrialN + 1  # QuestHandler counts from 0.

    # QUEST proposes a concentration to present,
    # but we usually don't have that particular one prepared.
    #
    # So we pick the one from our set which is closest to the proposed.
    print('QUEST-Proposed', concentration_proposed)
    concentration = find_nearest(concentration_steps, concentration_proposed)

    # If the concentration we selected is equal to the one previously presented ...
    #
    if concentration == previous_concentration:
        idx_previous_conc = get_bottle_index(concentration_steps,
                                             previous_concentration)

        # ... and we got a correct response ...
        if previous_detection_successful:
            # ... and we have not yet reached the lowest prepared concentration ...
            if idx_previous_conc < concentration_steps.size - 1:
                # ... move to a lower concentration!
                concentration = concentration_steps[idx_previous_conc + 1]
        # ... and we got an incorrect response ...
        else:
            # ... and we have not yet reached the highest prepared concentration ...
            if idx_previous_conc != 0:
                # ... more up to a higher concentration!
                concentration = concentration_steps[idx_previous_conc - 1]

    detection_successful = False

    msg = ('Threshold estimation for ' +
           exp_info['Substance'] +
           ', Trial ' +
           str(trial_number))
    vis_stimuli['staircase_info'].setText(msg)

    msg = ('\n\nPlease present bottle ' +
           str(get_bottle_index(concentration_steps, concentration) + 1) +
           '\n\n(' + str(np.round(10**concentration, decimals=5)) +
           ' g / 100 mL)')
    vis_stimuli['present_conc'].setText(msg)

    [s.draw() for s in [vis_stimuli['staircase_info'],
                        vis_stimuli['present_conc'],
                        vis_stimuli['detection_response'],
                        vis_stimuli['quit']]]
    win.flip()

    # Wait for keypress
    #
    event.clearEvents()
    keys = event.waitKeys(keyList=['y', 'n', 'q'])

    # We got a response. Clear the screen and wait for a short while
    # (so the user will actually notice the keypress was recognized).

    win.flip()
    core.wait(0.5)

    print(keys)
    if keys[0] == 'y':
        detection_successful = True
    elif keys[0] == 'n':
        detection_successful = False
    else:
        core.quit()

    quest_handler.addResponse(int(detection_successful), intensity=concentration)

    previous_concentration = concentration
    previous_detection_successful = detection_successful

    if trial_number >= min_trials:
        print('Adjusting stop interval to: ', 10**concentration * 1/2)
        quest_handler.stopInterval = 10**concentration * 1 / 2

    print('Confidence Interval:', quest_handler.confInterval(True))

    quest_handler.addOtherData('Concentration', 10**concentration)
    quest_handler.addOtherData('QUEST-Proposed Concentration',
                               10**concentration_proposed)
    exp_handler.nextEntry()

# Estimate, save and display the threshold
result = pd.DataFrame({'Participant': exp_info['Participant'],
                       'Substance':   exp_info['Substance'],
                       'Threshold':   [10**quest_handler.mean()]})

result.to_excel(path['threshold_filename'], index=False)
quest_handler.saveAsExcel(path['excel_filename'])

plot(intensities=np.power(10, quest_handler.intensities),
     responses=quest_handler.data,
     threshold=result['Threshold'].iloc[0],
     exp_info=exp_info,
     outfile=os.path.join(path['fig_dir'],
                          path['base_filename'] + '.pdf'))


msg = ('Estimated threshold for ' + exp_info['Substance'] + ': ' +
       str(np.round(10**result['Threshold'].values[0], decimals=5)) +
       ' g / 100 mL')
vis_stimuli['estimated_threshold'].setText(msg)
vis_stimuli['estimated_threshold'].draw()
vis_stimuli['quit'].draw()
win.flip()

event.waitKeys(keyList=['q'])
core.quit()

