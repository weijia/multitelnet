import mtel

def dummy():
    return

def main():
    
    import cProfile
    cProfile.run('mtel.execute(dummy)', 'fooprof')
    '''
    mtel.execute(dummy)
    '''
#-------------------------------------------------------------------------------


if __name__ == '__main__':
    main()