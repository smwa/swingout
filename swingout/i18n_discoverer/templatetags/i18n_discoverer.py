from django.template import Library, TemplateSyntaxError
from django.template.base import TokenType
from django.conf import settings
from django.templatetags import i18n
from i18n_discoverer.models import Message

__TRACK = bool(settings.I18N_DISCOVERER_TRACKING)

register = Library()

@register.tag('translate')
@register.tag('trans')
def do_translate(parser, token):
    if __TRACK:
        bits = token.split_contents()
        if len(bits) < 2:
            raise TemplateSyntaxError("'%s' takes at least one argument" % bits[0])
        message_string = parser.compile_filter(bits[1])
        remaining = bits[2:]

        message_context = None

        while remaining:
            option = remaining.pop(0)
            if option == 'context':
                try:
                    value = remaining.pop(0)
                except IndexError:
                    raise TemplateSyntaxError(
                        "No argument provided to the '%s' tag for the context option." % bits[0]
                    )
                if value in invalid_context:
                    raise TemplateSyntaxError(
                        "Invalid argument '%s' provided to the '%s' tag for the context option" % (value, bits[0]),
                    )
                message_context = parser.compile_filter(value)
        message_string = str(message_string)
        if message_string[0] == message_string[-1] == '"' or message_string[0] == message_string[-1] == "'":
            message_string = message_string[1:-1]
        __save(message_string, None, message_context)

    return i18n.do_translate(parser, token)

@register.tag("blocktranslate")
@register.tag("blocktrans")
def do_block_translate(parser, token):
    if __TRACK:
        bits = token.split_contents()

        options = {}
        remaining_bits = bits[1:]
        while remaining_bits:
            option = remaining_bits.pop(0)
            if option == 'with':
                value = i18n.token_kwargs(remaining_bits, parser)
                if not value:
                    raise TemplateSyntaxError('"with" in %r tag needs at least '
                                            'one keyword argument.' % bits[0])
            elif option == 'count':
                value = i18n.token_kwargs(remaining_bits, parser)
                if len(value) != 1:
                    raise TemplateSyntaxError('"count" in %r tag expected exactly '
                                            'one keyword argument.' % bits[0])
            elif option == "context":
                try:
                    value = remaining_bits.pop(0)
                    value = parser.compile_filter(value)
                except Exception:
                    raise TemplateSyntaxError(
                        '"context" in %r tag expected exactly one argument.' % bits[0]
                    )
            elif option == "asvar":
                value = remaining_bits.pop(0)
            options[option] = value

        if 'count' in options:
            countervar, counter = next(iter(options['count'].items()))
        else:
            countervar, counter = None, None
        if 'context' in options:
            message_context = options['context']
        else:
            message_context = None

        singular = []
        plural = []
        original_tokens = parser.tokens
        while parser.tokens:
            t = parser.next_token()
            if t.token_type in (TokenType.VAR, TokenType.TEXT):
                singular.append(t)
            else:
                break
        if countervar and counter and t.contents.strip() == 'plural':
            while parser.tokens:
                t = parser.next_token()
                if t.token_type in (TokenType.VAR, TokenType.TEXT):
                    plural.append(t)
                else:
                    break
        parser.tokens = original_tokens
        __save(' '.join(singular), ' '.join(plural), message_context)

    return i18n.do_block_translate(parser, token)

def __save(singular, plural=None, context=None):
    location = 'Templates'
    try:
        message = Message.objects.get(singular=singular, plural=plural, context=context, location=location)
    except Message.DoesNotExist:
        message = Message()
        message.singular = singular
        message.plural = plural
        message.context = context
        message.location = location
        message.save()
