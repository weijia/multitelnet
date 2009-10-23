import psyco
psyco.profile()
#psyco.log()
import mtel

def dummy():
  return

def main():
  if False:
    import cProfile
    cProfile.run('mtel.execute(dummy)', 'profileFile')
  else:
    mtel.execute(dummy)
#-------------------------------------------------------------------------------


if __name__ == '__main__':
    main()