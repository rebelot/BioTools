def getseq(accession_number, erase=False):
    if not erase:
        import urllib.request as url
        address = 'http://www.uniprot.org/uniprot/{}.fasta'.format(accession_number)
        file, _ = url.urlretrieve(address, '{}.fasta'.format(accession_number))
        with open(file) as seq_file:
            lines = seq_file.readlines()
            seq = ''.join(lines[1:]).replace('\n', '')
        url.urlcleanup()
        return seq
    if erase:
        while True:
            prompt = str.lower(input('Do you really want to delete FASTA files? [[y]/n]'))
            if prompt in ('y', 'yes'):
                import os
                file = accession_number+'.fasta'
                os.remove(file)
                print(file, 'Erased')
                return
            else:
                return

if __name__ == '__main__':
    prot = 'P01308'
    print(getseq(prot))
    #getseq(prot, erase=True)
    # P01130 Human LDL Receptor
    # Q99087 Xenopus laevis LDL Receptor 1