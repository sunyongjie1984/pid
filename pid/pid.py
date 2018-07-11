import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
fig, ax, sigOut, sigControl, maxControl = None, None, None, None, 0

def run( ):
    global ax, sigOut, sigControl
    ckt.tran1.run( )
    for sig in ckt.dataset().signals():
        if sig.name() == 'in':
            ax.plot( list(sig.x()), list(sig.y()), 'g', label=sig.name() )
        elif sig.name() == 'out':
            sigOut, = ax.plot( list(sig.x()), list(sig.y()), 'b', label=sig.name() )
        elif sig.name() == 'control':
            sigControl, = ax.plot( list(sig.x()), list(sig.y()), 'r', label=sig.name(), visible=False )

def rerun( ):
    global sigOut, maxControl
    ckt.tran1.run( )
    for sig in ckt.dataset().signals():
        if sig.name() == 'out' :
            sigOut.set_data( np.array(sig.x()), np.array(sig.y()) )
        elif sig.name() == 'control':
            sigControl.set_data( np.array(sig.x()), np.array(sig.y()) )
            maxControl = reduce( lambda a, b : a.real if ( a.real > b.real ) else b.real, sig.y() )
    plt.gcf().canvas.draw()

def main():
    global fig, ax
    fig, ax = plt.subplots()
    ax.set_ylim( [ -0.5, 1.5] )
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.set_window_title('PID Controller Demo')
    run()
    plt.show()

def press(event):
    global ax, sigControl, maxControl
    sys.stdout.write( 'press %s\r' % event.key )
    keyActions = {
            'P' : lambda : ckt.parameter('kp').update(ckt.parameter('kp').float()-0.1),
            'p' : lambda : ckt.parameter('kp').update(ckt.parameter('kp').float()+0.1),
            'I' : lambda : ckt.parameter('ki').update(ckt.parameter('ki').float()-10),
            'i' : lambda : ckt.parameter('ki').update(ckt.parameter('ki').float()+10),
            'D' : lambda : ckt.parameter('kd').update(ckt.parameter('kd').float()-10),
            'd' : lambda : ckt.parameter('kd').update(ckt.parameter('kd').float()+10),
            'b' : lambda: ckt.parameter('bypass').update( 0 if ckt.parameter('bypass').int() == 1 else 1 ),
            'n' : lambda: ckt.parameter('has_noise').update( 0 if ckt.parameter('has_noise').int() == 1 else 1 ),
            'c' : lambda: sigControl.set_visible( not sigControl.get_visible() ),
            }
    if event.key in keyActions:
        keyActions[ event.key ]()
    rerun()
    ax.set_title( 'kp=%.2f ki=%.2f kd=%.2f, maxControl=%.2f' % (
        ckt.parameter('kp').float(), ckt.parameter('ki').float(), ckt.parameter('kd').float(), maxControl.real ) )

if __name__ == "__main__":
    main( )
