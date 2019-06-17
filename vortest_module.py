"""Stellt Funktionen bereit, die Aufgaben für den Vortest
Mathematik generieren.
"""

from sympy import *

from random import randint, choice, shuffle

import os

init_session()


class TestMath:
    """Erstelle ein LaTeX Dokument mit berechneten Aufgaben."""

    def __init__(self, name, title):
        """Erstelle und öffne die beiden Dateien.
        name ist ein String, der an Ueb_ bzw. Lsg_ angehängt wird.
        title wird zwischen Übungen / Lösungen ... vom /today eingefügt.
        Derzeit eingebundene packages:
        [ngerman] babel
        [latin1] inputenc
        geometry (1cm überall außer unten, da 2cm)
        amsmath
        amsthm
        commath
        setspace
        Umgebung für (Lösungen von) Aufgaben ist __auf__
        """
        self.Uname = 'Ueb_{0}'.format(name)
        self.Lname = 'Lsg_{0}'.format(name)
        self.title = title
        self.Test = open('Uebungen\{0}.tex'.format(self.Uname), 'w')
        self.Test.write("""\\documentclass[10pt, a4paper]{article}\n
                \\usepackage[ngerman]{babel}
                \\usepackage[latin1]{inputenc}
                \\usepackage[left=1cm,right=1cm,top=1cm,bottom=2cm]{geometry}
                \\usepackage{amsmath, amsthm, commath, setspace}\n
                \\theoremstyle{definition}
                \\newtheorem{auf}{Aufgabe}\n
                \\begin{document}\n
                \\section*{Übungen """ + self.title + ' vom \\today}\n\n')

        self.Lsg = open('Uebungen\{0}.tex'.format(self.Lname), 'w')
        self.Lsg.write("""\\documentclass[10pt, a4paper]{article}\n
                \\usepackage[ngerman]{babel}
                \\usepackage[latin1]{inputenc}
                \\usepackage[left=1cm,right=1cm,top=1cm,bottom=2cm]{geometry}
                \\usepackage{amsmath, amsthm, commath, setspace}\n
                \\theoremstyle{definition}
                \\newtheorem{auf}{Lösung zu Aufgabe}\n
                \\begin{document}\n
                \\section*{Lösungen """ + self.title + ' vom \\today}\n\n')

    def final(self, cleanup=1, start=0):
        """Schließe die Dateien und kompiliere sie.
        Wenn cleanup=0 gesetzt wird, werden die TeX-Dateien nicht gelöscht.
        Wenn start=1 gesetzt wird, werden die PDFs geöffnet.
        """
        self.Test.write('\n\n\n \\section*{Viel Erfolg!} \n \\end{document}')
        self.Lsg.write('\n\n\n \\end{document}')
        self.Test.close()
        self.Lsg.close()
        os.system('pdflatex Uebungen\{0}.tex'.format(self.Uname))
        os.system('pdflatex Uebungen\{0}.tex'.format(self.Lname))
        os.system('del {0}.log'.format(self.Uname))
        os.system('del {0}.aux'.format(self.Uname))
        os.system('del {0}.log'.format(self.Lname))
        os.system('del {0}.aux'.format(self.Lname))
        if cleanup:
            os.system('del Uebungen\{0}.tex'.format(self.Uname))
            os.system('del Uebungen\{0}.tex'.format(self.Lname))
        else:
            pass
        os.system('move {0}.pdf Uebungen'.format(self.Uname))
        os.system('move {0}.pdf Uebungen'.format(self.Lname))
        if start:
            os.system('start Uebungen\{0}.pdf'.format(self.Uname))
            os.system('start Uebungen\{0}.pdf'.format(self.Lname))
        else:
            pass

    def lgsEq(self, dim=2, entryrange=6, resultrange=10, maxdet=10):
        """Erstelle eine Aufgabe, zur Übung von linearen Gleichungs-
        systemen. Dieses wird in Form von Gleichungen gegeben.
        dim gibt die anzahl der Variablen und Gleichungen an.
        entryrange gibt den maximalen Betrag der Koeffizienten an.
        resultrange gibt den maximalen Betrag der Ergebnisse an
        maxdet gibt den maximalen Betrag der Determinante an.
        """
        a, b, c, d, e, f = symbols('a b c d e f')
        vList = [a, b, c, d, e, f]
        A = Matrix([[randint(-entryrange, entryrange) for i in range(dim)]
                    for i in range(dim)])
        if A.det() != 0 and abs(A.det()) <= maxdet:
            pprint(A)
            usr = int(input('Soll diese Matrix behalten werden?' +
                            ' (0=nein, 1=ja) '))
        else:
            pass
        while (A.det() == 0 or abs(A.det()) > maxdet) or not(usr):
            A = Matrix([[randint(-entryrange, entryrange)
                        for i in range(dim)]
                        for i in range(dim)])
            if A.det() != 0 and abs(A.det()) <= maxdet:
                pprint(A)
                usr = int(input('Soll diese Matrix behalten werden?' +
                                ' (0=nein, 1=ja) '))
            else:
                pass
        R = Matrix([randint(-resultrange, resultrange) for i in range(dim)])
        B = A * R
        self.Test.write("""\\begin{auf}
            Lösen Sie das lineare Gleichungssystem: \n \\begin{align*} \n""")
        for i in range(dim):
            isfirst = 1
            for j in range(dim):
                if isfirst and A[i, j]:
                    if int(A[i, j]) == 1:
                        self.Test.write(latex(vList[j]))
                    elif int(A[i, j] == -1):
                        self.Test.write('- ' + latex(vList[j]))
                    else:
                        self.Test.write(latex(A[i, j]) + ' ' + latex(vList[j]))
                    isfirst = 0
                elif A[i, j].is_positive:
                    if int(A[i, j]) == 1:
                        self.Test.write(' + ' + latex(vList[j]))
                    else:
                        self.Test.write(' + ' + latex(A[i,j]) + ' ' +
                            latex(vList[j]))
                elif A[i, j].is_negative:
                    if int(A[i, j]) == -1:
                        self.Test.write(' - ' + latex(vList[j]))
                    else:
                        self.Test.write(' - ' + latex(-A[i,j]) + ' ' +
                            latex(vList[j]))
                else:
                    pass
            self.Test.write(' & = ' + latex(B[i]) + '\\\\\n')
        self.Test.write("\\end{align*} \n \\end{auf}\n\n")
        self.Lsg.write("\\begin{auf} \n $")
        for i in range(dim-1):
            self.Lsg.write(latex(vList[i]) + " = " + latex(R[i]) + ", ")
        self.Lsg.write(latex(vList[dim-1]) + " = " +
            latex(R[dim-1]) + " $. \n \\end{auf}\n\n")

    def lgsMat(self, dim=3, entryrange=6, resultrange=10, maxdet=10):
        """Erstelle eine Aufgabe, zur Übung von linearen Gleichungs-
        systemen. Dieses wird in Form von Matrizen gegeben. Zusätzlich zur
        Lösung soll / kann außerdem die Determinante der und die
        Inverse der Matrix berechnet werden.
        dim gibt die anzahl der Variablen und Gleichungen an.
        entryrange gibt den maximalen Betrag der Koeffizienten an.
        resultrange gibt den maximalen Betrag der Ergebnisse an
        maxdet gibt den maximalen Betrag der Determinante an.
        """
        A = Matrix([[randint(-entryrange, entryrange) for i in range(dim)]
                for i in range(dim)])
        if A.det() != 0 and abs(A.det()) <= maxdet:
            pprint(A)
            usr = int(input('Soll diese Matrix behalten werden?' +
                        ' (0=nein, 1=ja) '))
        else:
            pass
        while (A.det() == 0 or abs(A.det()) > maxdet) or not(usr):
            A = Matrix([[randint(-entryrange, entryrange)
                    for i in range(dim)]
                    for i in range(dim)])
            if A.det() != 0 and abs(A.det()) <= maxdet:
                pprint(A)
                usr = int(input('Soll diese Matrix behalten werden?' +
                            ' (0=nein, 1=ja) '))
            else:
                pass
        R = Matrix([randint(-resultrange, resultrange) for i in range(dim)])
        self.Test.write("""\\begin{auf}
            Gegeben ist das lineare Gleichungssystem \n $$""" +
            latex(A) +
            """\\cdot \\vec{x} = """ +
            latex(A*R) +
            """$$ \n Lösen Sie das lineare Gleichungssystem und berechnen Sie
            die Determinante sowie die Inverse der Matrix.\n \\end{auf}\n\n""")
        self.Lsg.write("\\begin{auf} \n Es gilt \n \\begin{spacing}{1.5} $$ " +
            latex(A.inv()) + "\\cdot" + latex(A*R) + "=" + latex(R) +
            "$$ \\end{spacing} \n und die Determinante ist $" + latex(A.det()) +
            "$. \n \\end{auf}\n\n")

    def parInt(self):
        """Erstelle eine Aufgabe, in der die Fläche zwischen einer Parabel
        und einer Geraden berechnet werden soll.
        """
        x = symbols('x')
        integ = 0
        while (integ > 200 or integ == 0):
            a = S(choice([1, 2, 3, 3, 4, 5, 6, 9, 12]))/choice([1, 1, 2, 3])
            nmbs = [choice([-1, 1])*a,
                randint(-10, 10), randint(-10, 10), randint(-10, 10),
                randint(-10, 10)]
            p = expand(nmbs[0]*(x-nmbs[1])*(x-nmbs[2])+(nmbs[3]*x + nmbs[4]))
            g = nmbs[3]*x+nmbs[4]
            integ = abs(integrate(p-g, (x, nmbs[1], nmbs[2])))
        self.Test.write("\\begin{auf} \n Berechnen Sie zu der Parabel $p(x)=" +
            latex(p) +
            "$ und der Geraden $g(x) = " +
            latex(g) +
            "$ die Schnittpunkte und die Fläche zwischen den Graphen. \n" +
            "\\end{auf} \n\n")
        self.Lsg.write("\\begin{auf} \n" +
            "Die Schnittpunkte sind $(" + latex(nmbs[1]) + "|" +
            latex(p.subs(x,nmbs[1])) + ")$ und $(" + latex(nmbs[2]) + "|" +
            latex(p.subs(x,nmbs[2])) + ")$ und der Flächeninhalt beträgt $" +
            latex(integ) + "$. \n \\end{auf} \n\n")

    def SP(self, count):
        """Erstelle eine Aufgabe, in der die Schnittpunkte zweier Parabeln
        berechnet werden sollen.
        count gibt die Anzahl der Teilaufgaben an.
        """
        x = symbols('x')
        self.Test.write("\\begin{auf} \n Berechnen Sie jeweils die " +
            "Schnittpunkte von der Parabel $p(x)$ und der Gerade $g(x)$.\n" +
            "\\begin{enumerate}\n")
        self.Lsg.write("\\begin{auf} \n Die Schnittpunkte sind: \n" +
            "\\begin{enumerate} \n")
        for i in range(count):
            a = S(choice([1, 2, 3, 3, 4, 5, 6, 9, 12]))/choice([1, 1, 2, 3])
            nmbs = [choice([-1, 1])*a,
                randint(-10, 10), randint(-10, 10), randint(-10, 10),
                randint(-10, 10)]
            p = expand(nmbs[0]*(x-nmbs[1])*(x-nmbs[2])+(nmbs[3]*x + nmbs[4]))
            g = nmbs[3]*x+nmbs[4]
            self.Test.write("\\item $p(x) = " + latex(p) +
                "$ und $g(x) = " + latex(g) +"$.\n")
            self.Lsg.write("\\item $(" + latex(nmbs[1]) + "|" +
                latex(p.subs(x,nmbs[1])) + ")$ und $(" + latex(nmbs[2]) + "|" +
                latex(p.subs(x,nmbs[2])) + ")$. \n")
        self.Test.write("\\end{enumerate} \n \\end{auf} \n\n")
        self.Lsg.write("\\end{enumerate} \n \\end{auf} \n\n")

    def quadG(self, count):
        """Erstelle eine Aufgabe, in der quadratische Gleichungen gelöst
        werden sollen.
        count gibt die Anzahl der Teilaufgaben an.
        """
        x = symbols('x')
        self.Test.write("\\begin{auf} \n Lösen Sie die quadratischen " +
            "Gleichungen nach $x$ auf.\n" +
            "\\begin{enumerate}\n")
        self.Lsg.write("\\begin{auf} \n Die Lösungen sind: \n" +
            "\\begin{enumerate} \n")
        for i in range(count):
            a = S(choice([1, 2, 3, 3, 4, 5, 6, 8, 9, 12]))/choice([1, 2, 3, 4])
            b = S(choice([0, 1, 2, 3, 3, 4, 5, 6, 9, 12]))/choice([1, 1, 2, 3])
            nmbs = [choice([-1, 1])*a,
                randint(-10, 10), randint(-10, 10), randint(-10, 10),
                randint(-10, 10), choice([-1,1])*b]
            qt1 = expand(nmbs[0]*(x-nmbs[1])*(x-nmbs[2]))
            qt2 = expand(nmbs[5]*(x-nmbs[3])*(x-nmbs[4]))
            ls = qt1 + qt2
            rs = qt2
            self.Test.write("\\item $" + latex(ls) +
                " = " + latex(rs) +" $.\n")
            self.Lsg.write("\\item $ x_1 = " + latex(nmbs[1]) +
                " $ und $ x_2 = " + latex(nmbs[2]) + "$. \n")
        self.Test.write("\\end{enumerate} \n \\end{auf} \n\n")
        self.Lsg.write("\\end{enumerate} \n \\end{auf} \n\n")

    def diffL(self, fList, vList=[-2, -1, 0, 1, 2]):
        """Erstelle eine Aufgabe, mit der Differenzieren geübt werden soll.
        In die Ableitung wird anschließend eine Zahl eingesetzt.
        fList ist eine Liste von Funktionen in der Variablen x, die abgeleitet
        werden sollen.
        vList gibt eine Liste von Zahlen, die eingesetzt werden könnten.
        """
        x = symbols('x')
        self.Test.write("""\\begin{auf} \n Berechnen Sie die Ableitungen der
            folgenden Funktionen und setzen Sie danach jeweils $ x_0 $ ein.\n
            \\begin{enumerate}\n""")
        X0 = []
        for Funk in fList:
            X0.append(choice(vList))
            self.Test.write("\\item $f(x) = " + latex(Funk) +
                "$ und $x_0 = " + latex(X0[-1]) + "$.\n")
        self.Test.write("\\end{enumerate} \n \\end{auf} \n\n")
        self.Lsg.write("""\\begin{auf} \n Die Lösungen sind: \n
            \\begin{enumerate} \n""")
        nmb = 0
        for Funk in fList:
            self.Lsg.write("\\item $f'(x) = " + latex(Funk.diff(x).simplify()) +
                "$ und $ f'(" + latex(X0[nmb]) + ") = " +
                latex(Funk.diff(x).subs(x, X0[nmb]).simplify()) +
                " \\approx " +
                latex(Funk.diff(x).subs(x, X0[nmb]).evalf().round(3)) +
                "$. \n")
            nmb += 1
        self.Lsg.write("\\end{enumerate} \n \\end{auf} \n\n")

    def intL(self, fList, vList=[-2, -1, 0, 1, 2]):
        """Erstelle eine Aufgabe, mit der Integrieren geübt werden soll.
        Nach dem unbestimmten Integral soll auch ein bestimmtes berechnet
        werden.
        fList ist eine Liste von Funktionen in der Variablen x, die integriert
        werden sollen.
        vList gibt eine Liste von Zahlen, die als untere Grenze für das
        Integral verwendet werden können. Die obere Grenze wird automatisch
        als +1, +2 oder +3 berechnet.
        """
        x = symbols('x')
        self.Test.write("""\\begin{auf} \n Berechnen Sie das Integral der
            folgenden Funktionen in den Grenzen $ (x_0 , x_1) $.\n
            \\begin{enumerate}\n""")
        X0 = []
        for Funk in fList:
            start = choice(vList)
            end = start + choice([1,2,3])
            X0.append((start, end))
            self.Test.write("\\item $\\int " + latex(Funk) +
                "\\dif x$ in den Grenzen $( " + latex(min(X0[-1])) + "," +
                latex(max(X0[-1])) + ")$.\n")
        self.Test.write("\\end{enumerate} \n \\end{auf} \n\n")
        self.Lsg.write("""\\begin{auf} \n Die Lösungen sind: \n
            \\begin{enumerate} \n""")
        nmb = 0
        for Funk in fList:
            self.Lsg.write("\\item $\\int f(x) \\dif x = " +
                latex(Funk.integrate(x).simplify()) +
                "$ und $ \\int_{" + latex(min(X0[nmb])) + "}^{" +
                latex(max(X0[nmb])) + "} f(x) \\dif x = " +
                latex(Funk.integrate(x).subs(x, max(X0[nmb])) -
                Funk.integrate(x).subs(x, min(X0[nmb]))) +
                " \\approx " +
                latex((Funk.integrate(x).subs(x, max(X0[nmb])) -
                    Funk.integrate(x).subs(x, min(X0[nmb]))).evalf().round(3)) +
                "$. \n")
            nmb += 1
        self.Lsg.write("\\end{enumerate} \n \\end{auf} \n\n")

    def bruch(self, count, primelist=[1, 2, 2, 2, 3, 3, 5, 7], difficulty=3):
        """Erstelle eine Aufgabe zum Üben von Bruchrechnnung.
        Jede Teilaufgabe enthält eine Strichrechnungs- und eine Punktrech-
        nungsaufgabe mit den gleichen Brüchen.
        count gibt die Anzahl der Teilaufgaben an.
        primelist ist die Auswahl der Primfaktoren, die für die Brüche ver-
        wendet werden. (Vielfachheit erhöht Wahrscheinlichkeit).
        difficulty gibt die Anzahl Primfaktoren an, die pro Zähler oder
        Nenner gewählt werden.
        """
        self.Test.write("""\\begin{auf} \n Berechnen Sie: \n
            \\begin{enumerate} \n""")
        self.Lsg.write("""\\begin{auf} \n Die Ergebnisse sind: \n
            \\begin{enumerate} \n""")
        for i in range(count):
            zlist = [choice(primelist) for j in range(difficulty * 3)]
            nlist = [choice(primelist) for j in range(difficulty * 3)]
            self.Test.write("\\item $ ")
            self.Lsg.write("\\item $ ")
            resadd = 0
            for j in range(3):
                zaehler = 1
                nenner = 1
                for k in range(difficulty):
                    zaehler *= zlist[3*j+k]
                    nenner *= nlist[3*j+k]
                if j == 0:
                    self.Test.write('\\frac{ ' + latex(zaehler) +
                        '}{' + latex(nenner) + '}')
                    resadd += S(zaehler) / nenner
                elif j == 1:
                    self.Test.write(' + \\frac{ ' + latex(zaehler) +
                        '}{' + latex(nenner) + '}')
                    resadd += S(zaehler) / nenner
                else:
                    self.Test.write(' - \\frac{ ' + latex(zaehler) +
                        '}{' + latex(nenner) + '}')
                    resadd -= S(zaehler) / nenner
            self.Test.write(' $ und $ ')
            self.Lsg.write(latex(resadd) + ' $ und $ ')
            resmult = 1
            for j in range(3):
                zaehler = 1
                nenner = 1
                for k in range(difficulty):
                    zaehler *= zlist[3*j+k]
                    nenner *= nlist[3*j+k]
                if j == 0:
                    self.Test.write('\\frac{ ' + latex(zaehler) +
                        '}{' + latex(nenner) + '}')
                    resmult *= S(zaehler) / nenner
                elif j == 1:
                    self.Test.write(' \\cdot \\frac{ ' + latex(zaehler) +
                        '}{' + latex(nenner) + '}')
                    resmult *= S(zaehler) / nenner
                else:
                    self.Test.write(' : \\frac{ ' + latex(zaehler) +
                        '}{' + latex(nenner) + '}')
                    resmult /= S(zaehler) / nenner
            self.Test.write(' $. \n')
            self.Lsg.write(latex(resmult) + ' $. \n')
        self.Test.write('\\end{enumerate} \n \\end{auf} \n\n')
        self.Lsg.write('\\end{enumerate} \n \\end{auf} \n\n')

    def loga(
            self, count, bases=[2, 3, 5], maxexp=[9, 5, 3],
            maxoffset=4, jitterlist=[7, 11, 13], weight=5):
        """Erstelle Aufgaben zum Üben von Logarithmen.
        count ist die Anzahl der Teilaufgaben.
        bases ist die Liste der für die Basis des Logarithmus zur
        Verfügung stehenden Primfaktoren.
        maxexp ist die korrespondierende Liste der für die Primfaktoren
        jeweils erlaubten maximalen Exponenten im Ergebnis.
        maxoffset gibt den Exponenten an, um den die Exponenten der Basis
        in Zähler und Nenner maximal erhöht werden, um Kürzung zu
        erfordern.
        jitterlist ist eine Liste von Primfaktoren, die zusätzlich in den
        Zähler und Nenner reinmultipliziert werden, um das Ergebnis
        komplizierter zu machen.
        weight gibt an, mit welchem Gewicht die nicht verwendeten Basen in
        die jitterlist eingerechnet werden.
        """
        self.Test.write('\\begin{auf} \n' +
            'Berechnen Sie die Logarithmen so weit es im Kopf geht. \n' +
            '\\begin{enumerate} \n')
        self.Lsg.write('\\begin{auf} \n' +
            'Die Ergebnisse sind: \n' +
            '\\begin{enumerate} \n')
        offsetlist = [o for o in range(maxoffset)]
        for i in range(count):
            base = choice(bases)
            notbase = [b for b in bases if b != base]
            for j in range(len(bases)):
                if base == bases[j]:
                    explist = [e + 1 for e in range(maxexp[j])]
                    result = choice([1, -1]) * choice(explist)
                else:
                    pass
            offset = choice(offsetlist)
            zjit = choice(weight * notbase + jitterlist)
            njit = choice(weight * notbase + jitterlist)
            if result > 0:
                zaehler = zjit * base**(result + offset)
                nenner = njit * base**offset
            else:
                zaehler = zjit * base**offset
                nenner = njit * base**(abs(result) + offset)
            self.Test.write('\\item $ \\log_' + latex(base) +
                ' \\frac{' + latex(zaehler) + '}{' + latex(nenner) +
                '} $ \n')
            self.Lsg.write('\\item $' + latex(result))
            if zjit == njit:
                self.Lsg.write('$ \n')
            else:
                self.Lsg.write(' + \\log_' + latex(base) + ' ' + latex(zjit) +
                    ' - \\log_' +  latex(base) + ' ' + latex(njit) +
                    ' $ \n')
        self.Test.write('\\end{enumerate} \n \\end{auf} \n \n ')
        self.Lsg.write('\\end{enumerate} \n \\end{auf} \n \n ')

    def potenz(self, count, gesExp=3, maxjit=2, factors=2):
        """Funktioniert noch nicht... :("""
        x, y, z = symbols('x y z')
        jitlist = [i for i in range(maxjit+1)]
        expchoice = [i + 1 for i in range(gesExp)]
        tListbase = [
            (x+1), (x+2), (x+3), (2*x+1), (2*x+3),
            (x-1), (x-2), (x-3), (2*x-1), (2*x-3),
            (y+1), (y+2), (y+3), (2*y+1), (2*y+3),
            (y-1), (y-2), (y-3), (2*y-1), (2*y-3),
            (z+1), (z+2), (z+3), (2*z+1), (2*z+3),
            (z-1), (z-2), (z-3), (2*z-1), (2*z-3),
            (x+y), (x+z), (y+z), (x*y+z), (x*z+y), (y*z+x),
            (x-y), (x-z), (y-z), (x*y-z), (x*z-y), (y*z-x)]
        tList1 = tListbase + [
            (x+1)**2, (x+2)**2, (x-1)**2, (x-2)**2, (x-1)*(x+1), (x-2)*(x+2),
            (y+1)**2, (y+2)**2, (y-1)**2, (y-2)**2, (y-1)*(y+1), (y-2)*(y+2),
            (z+1)**2, (z+2)**2, (z-1)**2, (z-2)**2, (z-1)*(z+1), (z-2)*(z+2),
            (x+y)**2, (x+z)**2, (y+z)**2, (x-y)**2, (x-z)**2, (y-z)**2,
            (x+y)*(x-y), (x+z)*(x-z), (y+z)*(y-z)]
        tList2 = tListbase + [
            (x**2+2*x+1), (x**2+4*x+4), (x**2-2*x+1), (x**2-4*x+4),
            (x**2-1), (x**2-4),
            (y**2+2*y+1), (y**2+4*y+4), (y**2-2*y+1), (y**2-4*y+4),
            (y**2-1), (y**2-4),
            (z**2+2*z+1), (z**2+4*z+4), (z**2-2*z+1), (z**2-4*z+4),
            (z**2-1), (z**2-4),
            (x**2+2*x*y+y**2), (x**2+2*x*z+z**2), (y**2+2*y*z+z**2),
            (x**2-2*x*y+y**2), (x**2-2*x*z+z**2), (y**2-2*y*z+z**2),
            (x**2-y**2), (x**2-z**2), (y**2-z**2)]
        choiceList = list(range(len(tList1)))
        self.Test.write('\\begin{auf} \n' +
            'Kürzen Sie so weit wie möglich und ' +
            'multiplizieren Sie dann aus. \n' +
            '\\begin{enumerate} \n')
        self.Lsg.write('\\begin{auf} \n' +
            'Das Ergebnis ist:' +
            '\\begin{enumerate} \n')
        for i in range(count):
            roll = choice([0, 1])
            if roll:
                tListZ = tList1
                tListN = tList2
            else:
                tListZ = tList2
                tListN = tList1
            shuffle(choiceList)
            index = choiceList[:factors]
            ZTerms = [tListZ[j] for j in index]
            NTerms = [tListN[j] for j in index]
            ZExp = [choice(expchoice) for j in range(factors)]
            NExp = [choice(expchoice) for j in range(factors)]
            ZExpRes = []
            NExpRes = []
            for L in [ZExp, NExp]:
                while sum(L) > gesExp:
                    k = choice(list(range(factors)))
                    if L[k] > 0:
                        L[k] -= 1
                    else:
                        pass
            for j in range(factors):
                jit = choice(jitlist)
                ZTerms.append(NTerms[j])
                NExpRes.append(NExp[j])
                NExp[j] += jit
                ZExp.append(jit)
            for j in range(factors):
                jit = choice(jitlist)
                NTerms.append(ZTerms[j])
                ZExpRes.append(ZExp[j])
                ZExp[j] += jit
                NExp.append(jit)
            permList = list(range(2*factors))
            shuffle(permList)
            ZTermFinal = [ZTerms[j] for j in permList]
            ZExpFinal = [ZExp[j] for j in permList]
            shuffle(permList)
            NTermFinal = [NTerms[j] for j in permList]
            NExpFinal = [NExp[j] for j in permList]
            self.Test.write('\\item $ \\frac{ ')
            for j in range(2*factors):
                if ZExpFinal[j] == 0:
                    pass
                elif ZExpFinal[j] == 1:
                    self.Test.write('(' + latex(ZTermFinal[j]) + ') ')
                else:
                    self.Test.write('(' + latex(ZTermFinal[j]) + ')^{' +
                        latex(ZExpFinal[j]) + '} ')
            self.Test.write('}{')
            for j in range(2*factors):
                if NExpFinal[j] == 0:
                    pass
                elif NExpFinal[j] == 1:
                    self.Test.write('(' + latex(NTermFinal[j]) + ') ')
                else:
                    self.Test.write('(' + latex(NTermFinal[j]) + ')^{' +
                        latex(NExpFinal[j]) + '} ')
            self.Test.write('}$ \n')
            Zaehler = 1
            Nenner = 1
            for j in range(factors):
                Zaehler *= ZTerms[j]**ZExpRes[j]
                Nenner *= NTerms[j]**NExpRes[j]
            self.Lsg.write('\\item $\\frac{' + latex(Zaehler.expand()) +
                '}{' + latex(Nenner.expand()) + '}$ \n')
        self.Test.write('\\end{enumerate} \n \\end{auf} \n \n ')
        self.Lsg.write('\\end{enumerate} \n \\end{auf} \n \n ')

    def koeffList(self, nmb, zero=0):
        """Erzeuge eine Koeffizientenliste, deren Betrag maximal nmb ist.
        Wird zero=1 gesetzt ist die 0 enthalten.
        """
        if zero:
            return ([i + 1 for i in range(nmb)] +
                [-i - 1 for i in range(nmb)] + [0])
        else:
            return ([i + 1 for i in range(nmb)] +
                [-i - 1 for i in range(nmb)])

    def polyDiv(
            self, count, guess=4, maxdenom=4, maxA=4, maxB=12, maxC=16,
            AjitR=8, BjitR=12, CjitR=16, jitx3=8):
        """Erstelle Aufgaben zur Polynomdivision -- Lösung einer Gleichung
        dritten Grades.
        count gibt die Anzahl der zu erstellenden Teilaufgaben an.
        guess gibt den maximalen Betrag der zu ratenden Nullstelle an.
        maxdenom gibt den größten Nenner an, der in der Gleichung vorkommt.
        Die anderen Variablen definieren Grenzen für die Koeffizienten des
        quadratischen Faktors (maxA, maxB, maxC) sowie die Koeffizienten der
        rechten Seite (AjitR, BjitR, CjitR, jitx3).
        """
        self.Test.write('\\begin{auf} \n Lösen Sie die Gleichungen. \n' +
            '\\begin{enumerate} \n')
        self.Lsg.write('\\begin{auf} \n Die Lösungen sind: \n' +
            '\\begin{enumerate} \n')
        x = symbols('x')
        guessL = self.koeffList(guess)
        denomL = [i + 1 for i in range(maxdenom)]
        AL = self.koeffList(maxA)
        BL = self.koeffList(maxB, zero=1)
        CL = self.koeffList(maxC)
        AjL = self.koeffList(AjitR, zero=1)
        BjL = self.koeffList(BjitR, zero=1)
        CjL = self.koeffList(CjitR, zero=1)
        j3L = self.koeffList(jitx3, zero=1)
        for i in range(count):
            X = choice(guessL)
            D = choice(denomL)
            A = choice(AL)
            B = choice(BL)
            C = choice(CL)
            Aj = choice(AjL)
            Bj = choice(BjL)
            Cj = choice(CjL)
            j3 = choice(j3L)
            LS = (1/S(D))*(x-X)*(A*x**2+B*x+C)+(j3*x**3+Aj*x**2+Bj*x+Cj)
            RS = j3*x**3+Aj*x**2+Bj*x+Cj
            self.Test.write('\\item $' + latex(LS.expand()) +
                ' = ' + latex(RS.expand()) + '$ \n')
            self.Lsg.write('\\item $ x_1 = ' + latex(X))
            if B**2-4*A*C < 0:
                self.Lsg.write(' $ \n')
            elif B**2-4*A*C == 0:
                self.Lsg.write(' , x_2 = ' + latex(-B/S(2*A)) + ' $ \n')
            else:
                lsg1 = (-B+sqrt(B**2-4*A*C))/S(2*A)
                lsg2 = (-B-sqrt(B**2-4*A*C))/S(2*A)
                self.Lsg.write(' , x_2 = ' + latex(lsg1.simplify()) +
                    ' \\approx ' + latex(lsg1.evalf().round(3)) +
                    ' , x_3 = ' + latex(lsg2.simplify()) +
                    ' \\approx ' + latex(lsg2.evalf().round(3)) + ' $ \n')
        self.Test.write('\\end{enumerate} \n \\end{auf} \n \n ')
        self.Lsg.write('\\end{enumerate} \n \\end{auf} \n \n ')

    def abl(self, count, maxexp=10, maxcoeff=9, maxdenom=6):
        x = symbols('x')
        explist = [i for i in range(maxexp+1)]
        coefflist = self.koeffList(maxcoeff, zero=1)
        denomlist = self.koeffList(maxdenom)
        self.Test.write('\\begin{auf}\n Leiten Sie ab.\n \\begin{enumerate}\n')
        self.Lsg.write('\\begin{auf}\n Die Ableitungen sind:' +
            '\n \\begin{enumerate}\n')
        for i in range(count):
            f = 0
            for s in explist[0:choice(explist[-len(explist)//2:])]:
                f += x**s * choice(coefflist) / S(choice(denomlist))
            self.Test.write('\\item $ f(x) = ' + latex(f) + '$\n')
            self.Lsg.write('\\item $ f\'(x) = ' + latex(f.diff(x)) + '$\n')
        self.Test.write('\\end{enumerate} \n \\end{auf} \n \n ')
        self.Lsg.write('\\end{enumerate} \n \\end{auf} \n \n ')
