import mido
import regulate_tracks


def get_channels_dict(input_msgs):
    """
    :param input_msgs: a list of all messages from an input song (along with their cumulative time)
    :return: a dictionary of all channels used in a song and their corresponding program
    """
    channels_dict = {}
    for i in range(len(input_msgs)):
        msg = input_msgs[i][0]
        if msg.type == "program_change":
            if msg.channel not in channels_dict.keys():
                channels_dict[msg.channel] = msg.program
    return channels_dict


def temp_function(input_msgs, channel): # this just gets the msgs (with cumulative time) for all of a particular channel
    channel_msgs = []
    for msg in input_msgs:
        if msg[0].type != "set_tempo":
            if msg[0].channel == channel:
                channel_msgs.append(msg)
    return channel_msgs


def notes_delays(channel_msgs):
    """
    :param channel_msgs: a list of all messages for a particular channel (within a song)
    :return: returns 2 lists of differences in cumulative time for all note on/off messages
    """
    note_on_difs, note_off_difs = [], []
    current_time_note_on, current_time_note_off = -1, -1
    """
    these 2 variables act as "temp" variables to get differences in time
    -1 is a placeholder value, is replaced as soon as get first note on/off msgs
    set at -1 as this could never be an actual time difference
    """
    for msg in channel_msgs:
        if msg[0].type == 'note_on':
            if current_time_note_on == -1:
                current_time_note_on = msg[1]
            else:
                note_on_difs.append(msg[1] - current_time_note_on)
                current_time_note_on = msg[1]
        elif msg[0].type == 'note_off':
            if current_time_note_off == -1:
                current_time_note_off = msg[1]
            else:
                note_off_difs.append(msg[1] - current_time_note_off)
                current_time_note_off = msg[1]
    return note_on_difs, note_off_difs


def make_velocity_dict(channel_msgs):
    velocity_dict = {}
    prev_velocity = -1
    for i in range(1, len(channel_msgs)):
        msg = channel_msgs[i][0]
        if msg.type == "note_on":
            if prev_velocity == -1:
                pass
            elif prev_velocity not in velocity_dict.keys():
                velocity_dict[prev_velocity] = [msg.velocity]
            else:
                velocity_dict[prev_velocity].append(msg.velocity)
            prev_velocity = msg.velocity
    return velocity_dict


def make_pitch_dict(channel_msgs):
    pitch_dict = {}
    prev_pitch = -1
    for i in range(1, len(channel_msgs)):
        msg = channel_msgs[i][0]
        if msg.type == "note_on":
            if prev_pitch == -1:
                pass
            elif prev_pitch not in pitch_dict.keys():
                pitch_dict[prev_pitch] = [msg.note]
            else:
                pitch_dict[prev_pitch].append(msg.note)
            prev_pitch = msg.note
    return pitch_dict


def main():
    output, ticksperbeat = regulate_tracks.main()
    list1 = output
    get_channels_dict(list1)
    channel_msgs = temp_function(list1, 2)
    notes_delays(channel_msgs)
    make_velocity_dict(channel_msgs)
    print(make_pitch_dict(channel_msgs))


if __name__ == '__main__':
    main()