from sopel import module
from emo.wdemotions import EmotionDetector

emo = EmotionDetector()

@module.rule('')

def hi(bot, trigger):
    print(trigger, trigger.nick)
    #
    # bot.say('Hi,this is just a text ' + trigger.nick)
    count = emo.detect_emotion_in_raw(str(trigger))
    print (count)


