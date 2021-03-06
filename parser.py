from display import *
from matrix import *
from draw import *

ARG_COMMANDS = [ 'line', 'scale', 'translate', 'xrotate', 'yrotate', 'zrotate', 'circle', 'bezier', 'hermite', 'sphere', 'box', 'torus']

def parse_file( f, points, transform, screen, color ):
    stack = []
    m = new_matrix()
    indent(m)
    stack.append(m)
    
    commands = f.readlines()

    c = 0
    while c  <  len(commands):
        cmd = commands[c].strip()
        if cmd in ARG_COMMANDS:
            c+= 1
            args = commands[c].strip().split(' ')
            i = 0
            while i < len( args ):
                args[i] = float( args[i] )
                i+= 1

            if cmd == 'line':
                add_edge( points, args[0], args[1], args[2], args[3], args[4], args[5] )
                
            elif cmd == 'circle':
                add_circle( points, args[0], args[1], 0, args[2], .01 )
            
            elif cmd == 'bezier':
                add_curve( points, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], .01, 'bezier' )
            
            elif cmd == 'hermite':
                add_curve( points, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], .01, 'hermite' )

            elif cmd == 'sphere':
                add_sphere( polygons, args[0], args[1], 0, args[2], 5 )

            elif cmd == 'torus':
                add_torus( polygons, args[0], args[1], 0, args[2], args[3], 5 )

            elif cmd == 'box':
                add_box( polygons, args[0], args[1], args[2], args[3], args[4], args[5] )


            elif cmd == 'scale':
                s = make_scale( args[0], args[1], args[2] )
                matrix_mult( stack[-1], s )
                stack[-1] = s
            elif cmd == 'translate':
                t = make_translate( args[0], args[1], args[2] )
                matrix_mult( stack[-1],t )
                stack[-1] = t

            else:
                angle = args[0] * ( math.pi / 180 )
                if cmd == 'xrotate':
                    r = make_rotX( angle )
                elif cmd == 'yrotate':
                    r = make_rotY( angle )
                elif cmd == 'zrotate':
                    r = make_rotZ( angle )
                matrix_mult( stack[-1], r )
                stack[-1] = r

        elif cmd == 'pop':
            stack.pop()

        elif cmd == 'push':
            stack.append(stack[-1])

        elif cmd == 'ident':
            ident( stack[-1] )
            
        elif cmd == 'apply':
            matrix_mult( stack[-1], points )

        elif cmd == 'clear':
            points = []

        elif cmd in ['display', 'save' ]:
            screen = new_screen()
            draw_polygons( points, screen, color )
            
            if cmd == 'display':
                display( screen )

            elif cmd == 'save':
                c+= 1
                save_extension( screen, commands[c].strip() )
        elif cmd == 'quit':
            return    
        elif cmd[0] != '#':
            print 'Invalid command: ' + cmd
        c+= 1
