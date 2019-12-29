import mido
mid = mido.MidiFile('major-scale.mid')


def add_cumulative_time(msg, currenttime):
    add_on = msg.time
    currenttime += add_on
    return currenttime


def main():
    currenttime = 0
    for i, track in enumerate(mid.tracks):
        print(f"Track {i}: {track.name}")
        for msg in track:
            print(msg)
            currenttime = add_cumulative_time(msg, currenttime)
            print(currenttime)

main()