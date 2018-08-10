__doc__ = """

Place a dummy atom at the center of mass of selected atoms.

"""

#Name: Center of Mass
#Command: pythonrun maestro_dummy_at_center_of_mass.dummy_center_of_mass

from schrodinger import maestro


def dummy_center_of_mass():
    """
    Place a dummy atom at the center of mass of selected atoms

    """

    sts = maestro.get_included_entries()
    asel = maestro.selected_atoms_get_asl()
    nst = maestro.analyze.create_new_structure()

    for st in sts:
        selected_atoms = maestro.analyze.get_atoms_from_asl(st, asel)
        for at in selected_atoms:
            nst.addAtom(at.element, at.x, at.y, at.z, at.atom_type)

    com = maestro.analyze.center_of_mass(nst)
    dummySt = maestro.analyze.create_new_structure()
    dummySt.addAtom("P", com[0], com[1], com[2], atom_type=150)

    pt = maestro.project_table_get()
    row = pt.importStructure(dummySt, name="COM")
    pt.includeRows([int(row.entry_id)], exclude_others=False)

    maestro.command('workspaceselectionreplace entry.id ' + row.entry_id)
    maestro.command('repatom rep=cpk at.selected')



if __name__ == "__main__":
    dummy_center_of_mass()
