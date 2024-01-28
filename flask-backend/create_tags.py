from classify import classify_tags
from transcribe_audio import create_timestamps, transcribe_to_sentence, transcribed_json

def make_overall_tag():
    tags_json = classify_tags()
    tags_dict = {}
    for i in tags_json:
        if i.prediction not in tags_dict.keys():
            tags_dict[i.prediction] = i.confidence
        else:
            tags_dict[i.prediction] += i.confidence
    overall_tag = ''
    max_conf = 0
    for i in tags_dict.keys():
        if tags_dict[i] >= max_conf:
            overall_tag = i
            max_conf = tags_dict[i]

    #print(overall_tag)
    return overall_tag

def make_tt_dict():
    tags_json = classify_tags()
    tags_list = []
    for i in tags_json:
        tags_list.append(i.prediction)
    timestamps_list = create_timestamps(transcribe_to_sentence(transcribed_json))
    tt_dict = dict(zip(timestamps_list, tags_list))

    #print(tt_dict)
    return tt_dict