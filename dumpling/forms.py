
import os
import re

from django.forms.fields import ChoiceField


class RelativePathField(ChoiceField):
    def __init__(self, path, match=None, recursive=False, allow_files=True,
                 allow_folders=False, required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        self.allow_files, self.allow_folders = allow_files, allow_folders
        super(RelativePathField, self).__init__(choices=(), required=required,
            widget=widget, label=label, initial=initial, help_text=help_text,
            *args, **kwargs)

        if self.required:
            self.choices = []
        else:
            self.choices = [("", "---------")]

        if self.match is not None:
            self.match_re = re.compile(self.match)

        pathlen = len(path)

        if recursive:
            for root, dirs, files in sorted(os.walk(self.path)):
                if self.allow_files:
                    for f in files:
                        if self.match is None or self.match_re.search(f):
                            f = os.path.join(root, f)[pathlen:]
                            self.choices.append((f, f.replace(path, "", 1)))
                if self.allow_folders:
                    for f in dirs:
                        if f == '__pycache__':
                            continue
                        if self.match is None or self.match_re.search(f):
                            f = os.path.join(root, f)[pathlen:]
                            self.choices.append((f, f.replace(path, "", 1)))
        else:
            try:
                for f in sorted(os.listdir(self.path)):
                    if f == '__pycache__':
                        continue
                    full_file = os.path.join(self.path, f)[pathlen:]
                    if (
                        (self.allow_files and os.path.isfile(full_file))
                        or
                        (self.allow_folders and os.path.isdir(full_file))
                    ) and (self.match is None or self.match_re.search(f)):
                        self.choices.append((full_file, f))
            except OSError:
                pass
