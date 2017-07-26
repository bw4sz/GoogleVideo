import argparse

def CommandArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path of single video",type=str,default='Test.tlv')
    parser.add_argument("--output", help="output directory",default="C:/MotionMeerkat")
    parser.add_argument("--draw", help="'Draw' or 'enter' object size",type=str,default='enter')
    parser.add_argument("--size", help="Minimum size of contour",default=0.001,type=float)
    parser.add_argument("--moglearning", help="Speed of MOG background detector, lowering values are more sensitive to movement",default=0.09,type=float)                                
    parser.add_argument("--mogvariance", help="Variance in MOG to select background",default=25,type=int)                                
    parser.add_argument("--crop", help="Set region of interest?",action='store_true')
    parser.add_argument("--todraw", help="Draw boxes to highlight motion'?",action="store_true")
    parser.add_argument("--show", help="Show frames as you process",action='store_true')
    parser.add_argument("--google_account", help="Path to google service account .json file",default="C:/Users/Ben/Dropbox/Google/MeerkatReader-9fbf10d1e30c.json")	    
    parser.add_argument("--bucket", help="Path to google service account .json file",default="api-project-773889352370-ml")	    
    
    args=parser.parse_args()
    return(args)
    