#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json_tricks
import numpy as np
import matplotlib.pyplot as plt
from psychopy import gui, core, data, visual


def check_if_file_exists(path):
    """
    Check if the file in the given path already exists.

    Parameters
    ----------
    path : str
        path to the file

    Returns
    -------
    bool
        Returns `True` if the file exists, and `False` otherwise.

    """
    if os.path.exists(path):
        dlg = gui.Dlg(title='Experiment Log File already exists!')
        dlg.addText('The file ' + path + 'already exists.')
        dlg.addText('Aborting!')
        dlg.show()

        return True
    else:
        return False


def gen_paths(exp_info):
    """
    Generate paths and filenames.

    Returns
    -------
    dict : path

    """
    base_dir = os.path.join(os.path.split(__file__)[0], os.path.pardir)
    data_dir = os.path.join(base_dir, 'Data')
    rawdata_dir = os.path.join(data_dir, 'Raw')
    fig_dir = os.path.join(base_dir, 'Figures')

    if not os.path.isdir(rawdata_dir):
        os.makedirs(rawdata_dir)

    if not os.path.isdir(fig_dir):
        os.makedirs(fig_dir)

    base_filename = gen_output_filename(exp_info)
    log_filename = os.path.join(rawdata_dir, base_filename + '.log')
    csv_filename = os.path.join(rawdata_dir, base_filename + '.csv')
    excel_filename = os.path.join(rawdata_dir, base_filename + '.xlsx')
    threshold_filename = os.path.join(
        data_dir,
        base_filename + ' - Threshold Estimate.xlsx'
    )
    metadata_filename = os.path.join(base_dir, '.metadata.yml')

    path = dict(base_dir=base_dir,
                data_dir=data_dir,
                rawdata_dir=rawdata_dir,
                fig_dir=fig_dir,
                base_filename=base_filename,
                log_filename=log_filename,
                csv_filename=csv_filename,
                excel_filename=excel_filename,
                threshold_filename=threshold_filename,
                metadata_filename=metadata_filename)

    return path


def gen_concentration_steps():
    """
    Generate the concentration_steps for the used solutions.

    Returns
    -------
    concentration_steps : dict
        Dictionary of dilutions steps.

    """
    sucrose_conc = np.logspace(np.log10(20),
                               np.log10(0.002510803515528001),
                               num=14, base=10)

    citric_acid_conc = np.logspace(np.log10(0.9),
                                   np.log10(0.00029031200707790503),
                                   num=14, base=10)

    sodium_chloride_conc = np.logspace(np.log10(2),
                                       np.log10(0.002),
                                       num=12, base=10)

    quinine_conc = np.logspace(np.log10(0.12255644907247643),
                               np.log10(1.5000000000000004e-05),
                               num=18, base=10)

    concentrations = {'Sucrose': sucrose_conc,
                      'Citric Acid': citric_acid_conc,
                      'Sodium Chloride': sodium_chloride_conc,
                      'Quinine Hydrochloride': quinine_conc}

    return concentrations


def get_start_val(substance):
    """
    Return the starting concentration for the specified substance.

    Parameters
    ----------
    substance : str
        The substance of interest

    Returns
    -------
    float
        The starting concentration.

    """
    c = gen_concentration_steps()

    start_val = {
        'Sucrose': c['Sucrose'][3],
        'Citric Acid': c['Citric Acid'][3],
        'Sodium Chloride': c['Sodium Chloride'][2],
        'Quinine Hydrochloride': c['Quinine Hydrochloride'][7]
    }

    return start_val[substance]


def get_exp_info(exp_info):
    """
    Retrieve experimental information and populate metadata dictionary.

    Returns
    -------
    exp_info : dict
        The experimental metadata.

    """
    exp_name = 'Gustatory Threshold Estimation'

    if exp_info:
        exp_info = {'Participant': exp_info['Participant'],
                    'Age': exp_info['Age'],
                    'Sex': exp_info['Sex'],
                    'Experimenter': exp_info['Experimenter'],
                    'Substance': list(gen_concentration_steps().keys()),
                    'Lateralization': ['none', 'left', 'right'],
                    'Method': ['QUEST'],
                    'Session': ['Test', 'Retest'],
                    'Exp. Version': '2018-04-06'}
    else:
        exp_info = {'Participant': '000',
                    'Age': '00',
                    'Sex': '',
                    'Substance': list(gen_concentration_steps().keys()),
                    'Lateralization': ['none', 'left', 'right'],
                    'Method': ['QUEST'],
                    'Session': ['Test', 'Retest'],
                    'Experimenter': '',
                    'Exp. Version': '2018-04-06'}

    dlg = gui.Dlg(title=exp_name)
    dlg.addText('\nParticipant Info', color='Red')
    dlg.addField('Participant', exp_info['Participant'])
    dlg.addField('Age', exp_info['Age'])
    dlg.addField('Sex', exp_info['Sex'])
    dlg.addText('\nExperiment Info', color='Red')
    dlg.addField('Substance', choices=exp_info['Substance'])
    dlg.addField('Lateralization', choices=exp_info['Lateralization'])
    dlg.addField('Method', choices=exp_info['Method'])
    dlg.addField('Session', choices=exp_info['Session'])
    dlg.addField('Experimenter', exp_info['Experimenter'])
    dlg.addFixedField('Exp. Version', exp_info['Exp. Version'])
    dlg.show()

    # If the 'Cancel' button was clicked...
    #
    if not dlg.OK:
        core.quit()

    # Now write the info we just acquired via the dialog box
    # to expInfo
    #
    for index, key in enumerate(dlg.inputFieldNames):
        exp_info[key] = dlg.data[index]

    exp_info['Date'] = data.getDateStr(format='%Y-%m-%d_%H%M')  # add a simple timestamp
    exp_info['expName'] = exp_name

    return exp_info


def load_exp_info():
    """
    Load experimental metadata from last run from disk.

    Returns
    -------
    dict or False
        Returns the experimental metadata, or `False` if the input file
        was not found.

    """

    base_dir = os.path.join(os.path.split(__file__)[0])
    exp_info_file = os.path.join(base_dir, '.metadata.json')

    try:
        with open(exp_info_file, 'r') as f:
            exp_info = json_tricks.load(f)
            exp_info['Date'] = data.getDateStr(format='%Y-%m-%d_%H%M')
    except FileNotFoundError:
        exp_info = False

    return exp_info


def save_exp_info(exp_info):
    """
    Save experimental metadata to disk.

    Parameters
    ----------
    exp_info : dict
        The experimental metadata.

    Returns
    -------
    bool
        `True` on success, `False` otherwise

    """
    base_dir = os.path.join(os.path.split(__file__)[0])
    exp_info_file = os.path.join(base_dir, '.metadata.json')

    try:
        with open(exp_info_file, 'w') as f:
            json_tricks.dump(exp_info, f)
        return True
    except Exception:
        return False


def gen_output_filename(exp_info):
    """
    Generate the base filename for the output files.

    Parameters
    ----------
    exp_info : dict
        A dictionary with experimental metadata. Must at least contain the
        keys `Participant`, `Substance`, `Method`, `Session`, and
        `Lateralization`.

    Returns
    -------
    filename : str
        The generated base filename.

    """
    if exp_info['Lateralization'] == 'none':
        filename = '%s - %s - %s - %s' % (exp_info['Participant'],
                                          exp_info['Substance'],
                                          exp_info['Method'],
                                          exp_info['Session'])
    else:
        filename = '%s - %s - %s - %s - %s' % (exp_info['Participant'],
                                               exp_info['Substance'],
                                               exp_info['Lateralization'],
                                               exp_info['Method'],
                                               exp_info['Session'])

    return filename


def get_bottle_index(steps, conc):
    """
    Get the index of a bottle corresponding to a concentration.

    Parameters
    ----------
    steps : array-like
        The concentration steps.

    conc : float
        The concentration for which to find the matching bottle index.

    Returns
    -------
    int
        The index of the bottle (zero-based).

    """
    return np.where(steps == conc)[0][0]


def gen_visual_stimuli(win):
    """
    Generate the visual stimuli for use in the experiment

    Parameters
    ----------
    win : psychopy.visual.Window
        The window the stimuli shall be bound to.

    Returns
    -------
    stimuli : dict
        The visual stimuli.

    """
    staircase_info = visual.TextStim(win, pos=(0, 1),
                                     alignVert='top', wrapWidth=80)
    present_conc = visual.TextStim(win, pos=(0, 0.3), bold=True,
                                   wrapWidth=80)

    msg = 'Did the participant recognize this concentration? [Y/N]'
    detection_response = visual.TextStim(win, pos=(0, -0.3), bold=True,
                                         text=msg,
                                         alignVert='bottom', wrapWidth=80)
    estimated_threshold = visual.TextStim(win)
    quit = visual.TextStim(win, pos=(0, -0.55),
                           text='(Press Q to quit.)')

    stimuli = dict(staircase_info=staircase_info,
                   present_conc=present_conc,
                   detection_response=detection_response,
                   estimated_threshold=estimated_threshold,
                   quit=quit)

    return stimuli


def find_nearest(a, a0):
    """
    Return the element in ndarray closest to a scalar value.

    Parameters
    ----------
    a : ndarray

    a0 : float

    Returns
    -------
    The element in `a` closest to the scalar `a0`.

    """
    idx = np.abs(a - a0).argmin()
    return a.flat[idx]


def plot(intensities, responses, threshold, exp_info, outfile):

    responses = np.array(responses)
    responses_yes_idx = np.where(responses == 1)[0]
    responses_no_idx = np.where(responses == 0)[0]

    fig, ax = plt.subplots()
    ax.plot(responses_yes_idx + 1, intensities[responses_yes_idx], 'gv', label='Yes')
    ax.plot(responses_no_idx + 1, intensities[responses_no_idx], 'r^', label='No')

    ax.axhline(threshold, color='red', lw=2)

    ax.set_yscale('log')
    ax.set_xlim([-0.25, (len(intensities) - 1) + 0.25])
    ax.grid(True)

    ax.set_title(
        '%s Threshold estimation for %s\nParticipant %s, Estimate: %6f'
        % (exp_info['Method'], exp_info['Substance'], exp_info['Participant'],
           threshold)
    )
    ax.set_xlabel('Trial')
    ax.set_ylabel('Stimulus Concentration in g / 100 mL')
    ax.legend(loc='upper right', numpoints=1)

    plt.savefig(outfile)
