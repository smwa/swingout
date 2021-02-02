from datetime import datetime

from django.core.management.commands import makemessages
from i18n_discoverer.models import Message

def write_pot_file(potfile, msgs):
    content = """# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: {}+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
""".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

    messages = {}
    for message in Message.objects.all():
        if message.singular not in messages:
            messages[message.singular] = {}
        if message.plural not in messages[message.singular]:
            messages[message.singular][message.plural] = {}
        if message.context not in messages[message.singular][message.plural]:
            messages[message.singular][message.plural][message.context] = []
        messages[message.singular][message.plural][message.context].append(message.location)
    
    def handle_quoted(message):
        message = message.replace('"', '\\"').replace("\n", '\\n')
        message = '"{}"'.format(message)
        return message

    for singular in messages:
        for plural in messages[singular]:
            for context in messages[singular][plural]:
                locations = messages[singular][plural][context]
                locations = [location.replace("\n", "\\n") for location in locations]
                locations = ' '.join(locations)
                singular_formatted = handle_quoted(singular)
                context_string = ''
                if context:
                    context_string = "msgctxt {}\n".format(handle_quoted(context))
                if not plural:
                    content += "\n#: {}\n{}msgid {}\nmsgstr \"\"\n".format(locations, context_string, singular_formatted)
                else:
                    plural_formatted = handle_quoted(plural)
                    content += "\n#: {}\n{}msgid {}\nmsgid_plural {}\nmsgstr[0] \"\"\nmsgstr[1] \"\"\n".format(locations, context_string, singular, plural_formatted)
    with open(potfile, 'w') as f:
        f.write(content)

makemessages.write_pot_file = write_pot_file

class Command(makemessages.Command):
    pass
