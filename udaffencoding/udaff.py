#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs
#import emote
import emojis
import emojis.db
import re

ALIAS_TO_EMOJI = emojis.db.get_emoji_aliases()
EMOJI_TO_ALIAS = dict((v, k) for k, v in ALIAS_TO_EMOJI.items())
EMOJI_TO_ALIAS_SORTED = sorted(ALIAS_TO_EMOJI.values(), key=len, reverse=True)

RE_TEXT_TO_EMOJI_GROUP = '({0})'.format('|'.join([re.escape(emoji) for emoji in ALIAS_TO_EMOJI]))
RE_TEXT_TO_EMOJI = re.compile(RE_TEXT_TO_EMOJI_GROUP)

RE_EMOJI_TO_TEXT_GROUP = u'({0})'.format(u'|'.join([re.escape(emoji) for emoji in EMOJI_TO_ALIAS_SORTED]))
RE_EMOJI_TO_TEXT = re.compile(RE_EMOJI_TO_TEXT_GROUP)

decoding_prefix = "ᛓ"
decoding_suffix = "ꖦ"
# TODO: Make regex non greedy
decoding_pattern_emo = re.compile("%s([\w\_-]+)%s" % (decoding_prefix, decoding_suffix))

decoding_langs = {
    ' and ': re.compile(u"(\sи\s)"),
    ' as ':  re.compile(u"(\sкак\s)"),
    'assert':  re.compile(u"(проверить)"),
    'break ':  re.compile(u"(прервать)"),
    'class':  re.compile(u"(класс)"),
    'continue':  re.compile(u"(продолжить)"),
    'def ': re.compile(u"(функция\s)"),
    'del':  re.compile(u"(удалить)"),
    'elif': re.compile(u"(ежели)"),
    'else': re.compile(u"(иначе)"),
    'except':  re.compile(u"(случись)"),
    'exec':  re.compile(u"(выполни)"),
    'finally':  re.compile(u"(наконец)"),
    'for ':  re.compile(u"(перебор\s)"),
    'from ':  re.compile(u"(из\s)"),
    'global ':  re.compile(u"(глобальное\s)"),
    'if ':  re.compile(u"(если\s)"),
    'import ':  re.compile(u"(подключить\s)"),
    ' in ':  re.compile(u"(\sв\s)"),
    ' is ':  re.compile(u"(\sсуть\s)"),
    'lambda':  re.compile(u"(лямбда)"),
    'not ':  re.compile(u"(не\s)"),
    ' or ':  re.compile(u"(\sили\s)"),
    'pass':  re.compile(u"(ничего)"),
    'print':  re.compile(u"(печать)"),
    'raise':  re.compile(u"(паника)"),
    'return':  re.compile(u"(вернуть)"),
    'try':  re.compile(u"(пробовать)"),
    'while':  re.compile(u"(повторять)"),
    'with':  re.compile(u"(пусть)"),
    'yield':  re.compile(u"(вернуть)"),
    'range':  re.compile(u"(интервал)"),
}

def keywords():
    keywords = []
    for good, re_ in decoding_langs.items():
        pattern = re_.pattern
        pattern = pattern.replace(u'\s','')
        pattern = pattern.replace(u' ','')
        pattern = pattern.replace(u'(','')
        pattern = pattern.replace(u')','')
        keywords.append(pattern)
    print(' | '.join(keywords))


def keywords2md():
    lines = ["| Английский | Русский |"]
    lines.append('|:--------|:----------|')
    keywords = []
    for good, re_ in decoding_langs.items():
        pattern = re_.pattern
        pattern = pattern.replace(u'\s','')
        pattern = pattern.replace(u' ','')
        pattern = pattern.replace(u'(','')
        pattern = pattern.replace(u')','')
        lines.append("| " + good + " | " + pattern + " |")
    print('\n'.join(lines))
    pass

# try:
#     # UCS-4
#     highpoints = re.compile(u'([\U00002600-\U000027BF])'
#                             '|([\U0001f300-\U0001f64F])'
#                             '|([\U0001f680-\U0001f6FF])')
# except re.error:
#     # UCS-2
#     print('UCS2')
#     highpoints = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')



class UdaffCodec(codecs.Codec):
    def encode(self, input, errors='strict'):
        Udaffs = decoding_pattern_emo.finditer(input)
        for Udaff in Udaffs:
            Udaff_string = Udaff.group(1)

            emo_ = None
            try:
                emo_ = emojis.encode(':'+Udaff_string+':')
                pass
            except:
                pass    
            if emo_:        
                input = input.replace(Udaff.group(0), 
                    #emote.lookup(Udaff_string)
                    emo_
                )
        return (input.encode('utf8'), len(input))

    def decode(self, input, errors='strict'):
        input_string = codecs.decode(input, 'utf8')
        # Udaffs = highpoints.finditer(input_string)

        # for Udaff in Udaffs:
        #     Udaff_string = Udaff.group(0)
        #     emoalias_ = emojis.decode(Udaff_string).replace(':','')
        #     substitute = "%s%s%s" % (decoding_prefix, 
        #                             # emote.decode(Udaff_string), 
        #                             emoalias_,
        #                             decoding_suffix)
        #     input_string = input_string.replace(Udaff_string, substitute)
        #     pass
        
        input_string = RE_EMOJI_TO_TEXT.sub(
                    lambda match: decoding_prefix + EMOJI_TO_ALIAS[match.group(0)][1:-1] + decoding_suffix, 
                    input_string)

        for good, re_ in decoding_langs.items():
            for term in re_.finditer(input_string):
                match = term.group(0)
                input_string = input_string.replace(match, good)    

        #print(input_string)
        # return input_string
        return (input_string, len(input))

class UdaffIncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return UdaffCodec().encode(input)

class UdaffIncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return UdaffCodec().decode(input)[0]

class UdaffStreamReader(UdaffCodec, codecs.StreamReader):
    pass

class UdaffStreamWriter(UdaffCodec, codecs.StreamWriter):
    pass

def search(encoding):
    if encoding == "udaff":
        return codecs.CodecInfo(
            name='udaff',
            encode=UdaffCodec().encode,
            decode=UdaffCodec().decode,
            incrementalencoder=UdaffIncrementalEncoder,
            incrementaldecoder=UdaffIncrementalDecoder,
            streamreader=UdaffStreamReader,
            streamwriter=UdaffStreamWriter,
        )
    return None

codecs.register(search)


