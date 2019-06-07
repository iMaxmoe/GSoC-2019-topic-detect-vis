import glob


def main():
    filenames = glob.glob('/home/vcla/Desktop/VCLA/cartago_news/tv/2015/*/*/*_US_*.txt')
    program_names = []
    filenames.sort()
    print len(filenames)

    for fname in filenames:
        print fname
        tmp = fname.split('/')[-1].split('.')[0].split('_')
        program = '_'.join(tmp[2:])
        print program
        if program not in program_names:
            program_names.append(program)
    program_names.sort()

    outf = open('program_names_all_cnn_fox_msnbc', 'w')
    for p in program_names:
        outf.write(p + '\n')
    outf.close()


if __name__ == '__main__':
    main()
