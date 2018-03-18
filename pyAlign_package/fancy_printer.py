def print_alignment(name_x, name_y, seq_x, seq_y, filename='Alignment'):
    ide = []
    for x, y in zip(seq_x, seq_y):
        if x == y:
            ide.append('|')
        elif x != y and x != '-' and y != '-':
            ide.append('.')
        else:
            ide.append(' ')

    ide= ''.join(ide)

    with open('{}.txt'.format(filename), 'x') as file:

        for chunk in range(0, len(seq_x), 70):
            file.write('{0:<7}{1:5d}    {2}    {3:<3d}\n'.format(name_x, chunk+1, seq_x[chunk:chunk+70], chunk + len(seq_x[chunk:chunk+70])))
            file.write('{0:<7}         {1}\n'.format(' '*7, ide[chunk:chunk+70]))
            file.write('{0:<7}         {1}\n'.format(name_y, seq_y[chunk:chunk+70]))

if __name__ == '__main__':
    name_x = "CYP26A1"
    name_y = "2VE3   "
    seq_x = "MFSWGLSCLSMLGAAGTALLCAGLLLGLAQQLWTLRWTLSRDWASTLPLPKGSMGWPFFGETLHWLVQGSRFHSSRRERYGTVFKTHLLGRPVIRVSGAENVRTILLGEHRLVRSQWPQSAHILLGSHTLLGAVGERHRQRRKVLARVFSRPALEQFVPRLQEALRREVRSWCAA.QRPVAVYQAAKALTFRMAARILLGLQLDEA....RCTELAQTFERLVENLFSLPLDVPFSGLRKGIRARDQLYQHLDEVIAEKLREELTAEP....GDALHLIINSARELGRELSVQELKELAVELLFAAFFTTASASTSLILLLLQHPAAIAKIQQELSAQGLGSPCSCAPRASGSRPDCSCEPDLSLAVLGRLRYVDCVVKEVLRLLPPVSGGYRTALRTFELDGYQIPKGWSVMYSIRDTHETAAVYRSPPEGFDPERFGVESEDARGSGGRFHYIPFGGGARSCLGQELAQAVLQLLAVELVRTARWELATPAFPVMQTVPIVHPVDGLLLLFHPLPTLGAGDGSPF........"
    seq_y = "............................................NSLPIPPGDFGLPWLGETLNFLNDG.DFGKKRQQQFGPIFKTRLFGKNVIFISGALANRFLFTKEQETFQATWPLSTRILLGPNALATQMGEIHRSRRKILYQAFLPRTLDSYLPKMDGIVQGYLEQWGKA..NEVIWYPQLRRMTFDVAATLFMGEKVSQ......NPQLFPWFETYIQGLFSLPIPLPNTLFGKSQRARALLLAELEKIIKARQQQPPS......EEDALGILLAARDDNNQPLSLPELKDQILLLLFAGHETLTSALSSFCLLLGQHSDIRERVRQEQNKLQL...................SQELTAETLKKMPYLDQVLQEVLRLIPPVGGGFRELIQDCQFQGFHFPKGWLVSYQISQTHADPDLYPDP.EKFDPERFTPDG..SATHNPPFAHVPFGGGLRECLGKEFARLEMKLFATRLIQQFDWTLLPGQNLELVVTPSPRPKDNLRVKLHSL..................."
    print_alignment(name_x, name_y, seq_x.replace(".","-"), seq_y.replace(".","-"), "26c1")