from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from string import ascii_uppercase
from kivy.utils import platform
from os import listdir

if platform == 'win':
    from ctypes import windll, create_unicode_buffer, c_wchar_p, sizeof

class TestBox(BoxLayout):
    pass


class FCTest(App):
    def get_win_drive_names(self):
        volumeNameBuffer = create_unicode_buffer(1024)
        fileSystemNameBuffer = create_unicode_buffer(1024)
        serial_number = None
        max_component_length = None
        file_system_flags = None
        drive_names = []
        #  Get the drive letters, then use the letters to get the drive names
        bitmask = (bin(windll.kernel32.GetLogicalDrives())[2:])[::-1]  # strip off leading 0b and reverse
        drive_letters = [ascii_uppercase[i] + ':/' for i, v in enumerate(bitmask) if v == '1']

        for d in drive_letters:
            rc = windll.kernel32.GetVolumeInformationW(c_wchar_p(d), volumeNameBuffer, sizeof(volumeNameBuffer),
                                                       serial_number, max_component_length, file_system_flags,
                                                       fileSystemNameBuffer, sizeof(fileSystemNameBuffer))
            if rc:
                drive_names.append(f'{volumeNameBuffer.value}({d[:2]})')
        return drive_names

    def get_drive_names(self):
        if platform == 'win':
            names = self.get_win_drive_names()
        elif platform == 'macosx':
            names = listdir('/Volumes')
        else:
            names = ['ERROR']  # raise exception?
        return names


if __name__ == '__main__':
    FCTest().run()
