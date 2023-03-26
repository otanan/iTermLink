#!/usr/bin/env python3
"""iTerm2 API wrapper with additional functionality provided.

**Author: Jonathan Delgado**

"""
#======================== Imports ========================#
import iterm2
import time # session title
import plistlib # color presets
from pathlib import Path
import AppKit # launching and checking the status of iTerm
#--- Custom imports ---#
from itermlink.tools.console import *
#======================== Async ========================#

#------------- Miscellaneous -------------#
async def set_title(iterm_obj, title):
    """ Sets the title to the iTerm object depending on what type it is. """
    async def set_session_title(sess, title):
        # Set session title
        update = iterm2.LocalWriteOnlyProfile()
        update.set_allow_title_setting(False)
        update.set_name(title)
        # Sleep needed since running it immediately won't work
        time.sleep(0.7)
        await sess.async_set_profile_properties(update)

    if isinstance(iterm_obj, iterm2.tab.Tab):
        await iterm_obj.async_set_title(title)
    elif isinstance(iterm_obj, iterm2.session.Session):
        await set_session_title(iterm_obj, title)


async def cleared_command(sess, command):
    """ Clears the screen then runs the provided command. """
    await sess.async_send_text(f'clear && {command}\n')


async def get_visible_history(sess):
    """ Gets the lines of text representing the session's visible history. """
    contents = await sess.async_get_screen_contents()

    return [
        contents.line(i).string for i in range(contents.number_of_lines)
        # Remove trailing empty lines for new sessions
        if contents.line(i).string != ''
    ]


#------------- Sessions -------------#
async def all_sessions_info(windows):
    """ Gets information relevant to all current sessions. """
    info = []
    for window in windows:
        for tab in window.tabs:
            for sess in tab.all_sessions:
                info.append({
                    'session': sess,
                    'path': Path(
                        await sess.async_get_variable('path')
                    ).resolve(),
                    'profile': await sess.async_get_profile()
                })

    return info


#------------- Color presets -------------#
async def get_current_preset(connection, profile=None):
    """ Get the color preset the profile uses if any.
    
        Kwargs:
            profile: the profile to check, None will use the default profile.
    
        Returns:
            (None): none
    
    """
    #--- Helper functions ---#
    def colors_unequal(profile_color, preset_color):
        """ Compare the profile color to preset color. """
        return (round(profile_color.red) != round(preset_color.red) or
            round(profile_color.green) != round(preset_color.green) or
            round(profile_color.blue) != round(preset_color.blue) or
            round(profile_color.alpha) != round(preset_color.alpha) or
            profile_color.color_space != preset_color.color_space)

    def profile_uses_preset(profile, preset):
        """ Compare each of the profile's colors to the preset's colors. """
        for preset_color in preset.values:
            profile_color = profile.get_color_with_key(preset_color.key)
            # Check all colors
            if colors_unequal(profile_color, preset_color):
                return False
        return True

    if profile is None:
        profile = await iterm2.Profile.async_get_default(connection)
    
    presets = await iterm2.ColorPreset.async_get_list(connection)
    for preset_name in presets:
        preset = await iterm2.ColorPreset.async_get(connection, preset_name)
        if profile_uses_preset(profile, preset):
          return preset_name
    return None


async def change_preset(connection, preset_name, profile=None):
    """ Change main profile color scheme by the scheme name. """
    if profile is None:
        profile = await iterm2.Profile.async_get_default(connection)
    
    # Get the color scheme
    preset = await iterm2.ColorPreset.async_get(connection, preset_name)
    await profile.async_set_color_preset(preset)


async def get_presets(connection):
    return await iterm2.ColorPreset.async_get_list(connection)


async def get_current_session(connection):
    app = await iterm2.async_get_app(connection)
    return app.current_window.current_tab.current_session


#======================== Sync ========================#

# def focus(sess=None):
#     """ Pull the provided session, or current session to the front. """
#     async def _focus_helper(connection):
#         nonlocal sess
#         # Default to the current session
#         if sess is None: sess = await get_current_session(connection)

#         await sess.async_activate(order_window_front=True)

#     iterm2.run_until_complete(_focus_helper)


def cd(path, sess=None):
    """ Changes the current working directory of the iTerm session. """
    async def _cd_helper(connection):
        nonlocal sess
        # Default to the current session
        if sess is None: sess = await get_current_session(connection)

        await sess.async_send_text(f'cd "{path}"\n')

    iterm2.run_until_complete(_cd_helper)


def run_command_on_active_sess(command, sess=None):
    """ Runs the following command on active session. """
    async def _run_command_helper(connection):
        nonlocal sess
        # Default to the current session
        if sess is None: sess = await get_current_session(connection)

        await sess.async_send_text(f'{command}\n')

    iterm2.run_until_complete(_run_command_helper)


def delete_preset(preset_name):
    """ Delete preset name. """
    colors_fname = Path.home() / 'Library/Preferences/com.googlecode.iterm2.plist'

    with open(colors_fname, 'rb') as f: pl = plistlib.load(f)

    del pl['Custom Color Presets'][preset_name]
    # Update file with changes
    with open(colors_fname, 'wb') as f: plistlib.dump(pl, f)


def has_unique_session(window):
    """ Returns True if there is only one session in this window. """
    return len(window.tabs) == 1 and len(window.current_tab.sessions) == 1


def is_iterm_running():
    """ Checks if iTerm is running. """
    # Returns an empty tuple if iTerm is not running
    return AppKit.NSRunningApplication.runningApplicationsWithBundleIdentifier_('com.googlecode.iterm2') != ()


def launch_iterm():
    """ Launch iTerm app. """
    AppKit.NSWorkspace.sharedWorkspace().launchApplication_('iTerm')

#======================== Entry ========================#


def main():
    print('itermlink.py')
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print('Keyboard interrupt.')