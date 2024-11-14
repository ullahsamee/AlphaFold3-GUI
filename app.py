import streamlit as st
import json
import re
import os
import subprocess
from PIL import Image

def run_alphafold(command):
    """
    Runs the AlphaFold Docker command and captures output.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    output_lines = []
    for line in iter(process.stdout.readline, ''):
        if line:
            output_lines.append(line)
    process.stdout.close()
    process.wait()
    return ''.join(output_lines)

def main():
    # Set page configuration with custom theme
    st.set_page_config(
        page_title="AFusion: AlphaFold 3 GUI",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Remove padding */
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        /* Header styling */
        .css-10trblm {
            font-size: 2rem;
            color: #2c3e50;
        }
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f2f4f5;
        }
        /* Button styling */
        .stButton>button {
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #2c3e50;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title and subtitle
    st.markdown("<h1 style='text-align: center;'>🔬 AFusion: AlphaFold 3 GUI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 16px;'>A convenient GUI for running AlphaFold 3 predictions</p>", unsafe_allow_html=True)

    #### Sidebar Outline ####
    with st.sidebar:
        st.header("Navigation")
        sections = {
            "Job Settings": "job_settings",
            "Sequences": "sequences",
            "Bonded Atom Pairs": "bonded_atom_pairs",
            "User Provided CCD": "user_ccd",
            "Generated JSON": "json_content",
            "Execution Settings": "execution_settings",
            "Run AlphaFold 3": "run_alphafold",
        }
        for section_name, section_id in sections.items():
            st.markdown(f"<a href='#{section_id}' style='text-decoration: none;'>{section_name}</a>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<small>Created by Mars 2024.</small>", unsafe_allow_html=True)

    # Main Content
    st.markdown('<div id="home"></div>', unsafe_allow_html=True)
    st.markdown("### Welcome to AFusion!")
    st.write("Use this GUI to generate input JSON files and run AlphaFold 3 predictions with ease.")

    st.markdown('<div id="job_settings"></div>', unsafe_allow_html=True)
    st.header("📝 Job Settings")
    with st.expander("Configure Job Settings", expanded=True):
        job_name = st.text_input("Job Name", value="My AlphaFold Job", help="Enter a descriptive name for your job.")
        model_seeds = st.text_input("Model Seeds (comma-separated)", value="1,2,3", help="Provide integer seeds separated by commas.")
        model_seeds_list = [int(seed.strip()) for seed in model_seeds.split(",") if seed.strip().isdigit()]
        if not model_seeds_list:
            st.error("Please provide at least one valid model seed.")
            st.stop()

    st.markdown('<div id="sequences"></div>', unsafe_allow_html=True)
    st.header("📄 Sequences")
    sequences = []
    num_entities = st.number_input("Number of Entities", min_value=1, step=1, value=1, help="Select the number of entities you want to add.")

    for i in range(int(num_entities)):
        st.markdown(f"### Entity {i+1}")
        with st.expander(f"Entity {i+1} Details", expanded=True):
            entity_type = st.selectbox(f"Select Entity Type", ["Protein 🧬", "RNA 🧫", "DNA 🧬", "Ligand 💊"], key=f"entity_type_{i}")
            entity_id = st.text_input(f"Entity ID (Entity {i+1})", key=f"entity_id_{i}", help="Provide entity ID(s), separated by commas if multiple.")
            entity_ids = re.split(r"\s*,\s*", entity_id)  # Split by commas

            if not entity_id:
                st.error("Entity ID is required.")
                continue  # Skip to the next entity

            if entity_type.startswith("Protein"):
                protein_entry = handle_protein_entity(i, entity_ids)
                if protein_entry:
                    sequences.append({"protein": protein_entry})
            elif entity_type.startswith("RNA"):
                rna_entry = handle_rna_entity(i, entity_ids)
                if rna_entry:
                    sequences.append({"rna": rna_entry})
            elif entity_type.startswith("DNA"):
                dna_entry = handle_dna_entity(i, entity_ids)
                if dna_entry:
                    sequences.append({"dna": dna_entry})
            elif entity_type.startswith("Ligand"):
                ligand_entry = handle_ligand_entity(i, entity_ids)
                if ligand_entry:
                    sequences.append({"ligand": ligand_entry})
            else:
                st.error(f"Unknown entity type: {entity_type}")

    st.markdown('<div id="bonded_atom_pairs"></div>', unsafe_allow_html=True)
    st.header("🔗 Bonded Atom Pairs (Optional)")
    bonded_atom_pairs = []
    add_bonds = st.checkbox("Add Bonded Atom Pairs")
    if add_bonds:
        num_bonds = st.number_input("Number of Bonds", min_value=1, step=1, key="num_bonds")
        for b in range(int(num_bonds)):
            st.markdown(f"**Bond {b+1}**")
            bond = handle_bond(b)
            if bond:
                bonded_atom_pairs.append(bond)

    st.markdown('<div id="user_ccd"></div>', unsafe_allow_html=True)
    st.header("🧩 User Provided CCD (Optional)")
    user_ccd = st.text_area("User CCD (mmCIF format)")

    # Generate JSON Data
    alphafold_input = {
        "name": job_name,
        "modelSeeds": model_seeds_list,
        "sequences": sequences,
        "dialect": "alphafold3",
        "version": 1
    }

    if bonded_atom_pairs:
        alphafold_input["bondedAtomPairs"] = bonded_atom_pairs

    if user_ccd:
        alphafold_input["userCCD"] = user_ccd

    st.markdown('<div id="json_content"></div>', unsafe_allow_html=True)
    st.header("📄 Generated JSON Content")
    json_output = json.dumps(alphafold_input, indent=2)
    st.code(json_output, language="json")

    st.markdown('<div id="execution_settings"></div>', unsafe_allow_html=True)
    st.header("⚙️ AlphaFold 3 Execution Settings")
    with st.expander("Configure Execution Settings", expanded=True):
        # Paths for Docker command
        af_input_path = st.text_input("AF Input Path", value=os.path.expanduser("~/af_input"), help="Path to AlphaFold input directory.")
        af_output_path = st.text_input("AF Output Path", value=os.path.expanduser("~/af_output"), help="Path to AlphaFold output directory.")
        model_parameters_dir = st.text_input("Model Parameters Directory", value="/path/to/models", help="Path to model parameters directory.")
        databases_dir = st.text_input("Databases Directory", value="/path/to/databases", help="Path to databases directory.")

        # Additional options
        run_data_pipeline = st.checkbox("Run Data Pipeline (CPU only, time-consuming)", value=True)
        run_inference = st.checkbox("Run Inference (requires GPU)", value=True)

    st.markdown('<div id="run_alphafold"></div>', unsafe_allow_html=True)
    st.header("🚀 Run AlphaFold 3")
    # Save JSON to file
    if st.button("Save JSON File"):
        json_save_path = os.path.join(af_input_path, "fold_input.json")
        try:
            os.makedirs(af_input_path, exist_ok=True)
            with open(json_save_path, "w") as json_file:
                json.dump(alphafold_input, json_file, indent=2)
            st.success(f"JSON file saved to {json_save_path}")
        except Exception as e:
            st.error(f"Error saving JSON file: {e}")

    # Run AlphaFold 3
    if st.button("Run AlphaFold 3 Now ▶️"):
        json_save_path = os.path.join(af_input_path, "fold_input.json")
        try:
            # Ensure JSON is saved before running
            os.makedirs(af_input_path, exist_ok=True)
            with open(json_save_path, "w") as json_file:
                json.dump(alphafold_input, json_file, indent=2)
        except Exception as e:
            st.error(f"Error saving JSON file: {e}")
            st.stop()

        # Build the Docker command
        docker_command = (
            f"docker run -it "
            f"--volume {af_input_path}:/root/af_input "
            f"--volume {af_output_path}:/root/af_output "
            f"--volume {model_parameters_dir}:/root/models "
            f"--volume {databases_dir}:/root/public_databases "
            f"--gpus all "
            f"alphafold3 "
            f"python run_alphafold.py "
            f"--json_path=/root/af_input/fold_input.json "
            f"--model_dir=/root/models "
            f"--output_dir=/root/af_output "
            f"{'--run_data_pipeline' if run_data_pipeline else ''} "
            f"{'--run_inference' if run_inference else ''}"
        )

        st.markdown("#### Docker Command:")
        st.code(docker_command, language="bash")

        # Run the command and display output in a box
        with st.spinner('AlphaFold 3 is running...'):
            output = run_alphafold(docker_command)

        st.success("AlphaFold 3 execution completed.")

        # Display the output in an expander box
        st.markdown("#### Command Output:")
        with st.expander("Show Command Output 📄", expanded=False):
            st.text_area("Command Output", value=output, height=400)
    else:
        st.info("Click the 'Run AlphaFold 3 Now ▶️' button to execute the command.")

    st.markdown("---")
    # Add footer
    st.markdown("<p style='text-align: center; font-size: 12px; color: #95a5a6;'>© 2024 Mars. All rights reserved.</p>", unsafe_allow_html=True)

def handle_protein_entity(i, entity_ids):
    sequence = st.text_area(f"Protein Sequence (Entity {i+1})", key=f"sequence_{i}", help="Enter the protein sequence.")
    # Modifications
    modifications_list = []
    add_modifications = st.checkbox(f"Add Modifications", key=f"add_modifications_{i}")
    if add_modifications:
        num_modifications = st.number_input(f"Number of Modifications", min_value=1, step=1, key=f"num_modifications_{i}")
        for j in range(int(num_modifications)):
            st.markdown(f"**Modification {j+1}**")
            mod_col1, mod_col2 = st.columns(2)
            with mod_col1:
                mod_type = st.text_input(f"Modification Type (ptmType)", key=f"mod_type_{i}_{j}")
            with mod_col2:
                mod_position = st.number_input(f"Modification Position (ptmPosition)", min_value=1, step=1, key=f"mod_position_{i}_{j}")
            modifications_list.append({"ptmType": mod_type, "ptmPosition": mod_position})

    # MSA Options
    msa_option = st.selectbox(f"MSA Option", ["Auto-generate 🛠️", "Don't use MSA 🚫", "Upload MSA 📄"], key=f"msa_option_{i}")
    if msa_option == "Upload MSA 📄":
        unpaired_msa = st.text_area(f"Unpaired MSA", key=f"unpaired_msa_{i}")
    elif msa_option == "Don't use MSA 🚫":
        unpaired_msa = ""
    else:
        unpaired_msa = None  # Auto-generate

    # Templates
    templates_list = []
    add_templates = st.checkbox(f"Add Templates", key=f"add_templates_{i}")
    if add_templates:
        num_templates = st.number_input(f"Number of Templates", min_value=1, step=1, key=f"num_templates_{i}")
        for k in range(int(num_templates)):
            st.markdown(f"**Template {k+1}**")
            mmcif_content = st.text_area(f"mmCIF Content", key=f"mmcif_{i}_{k}")
            query_indices = st.text_input(f"Query Indices List (comma-separated)", key=f"query_indices_{i}_{k}")
            template_indices = st.text_input(f"Template Indices List (comma-separated)", key=f"template_indices_{i}_{k}")
            try:
                query_indices_list = [int(idx.strip()) for idx in query_indices.split(",") if idx.strip()]
                template_indices_list = [int(idx.strip()) for idx in template_indices.split(",") if idx.strip()]
            except ValueError:
                st.error("Indices lists should be integers separated by commas.")
                query_indices_list = []
                template_indices_list = []
            templates_list.append({
                "mmcif": mmcif_content,
                "queryIndices": query_indices_list,
                "templateIndices": template_indices_list
            })

    protein_entry = {
        "id": entity_ids if len(entity_ids) > 1 else entity_ids[0],
        "sequence": sequence
    }
    if modifications_list:
        protein_entry["modifications"] = modifications_list
    if unpaired_msa is not None:
        protein_entry["unpairedMsa"] = unpaired_msa
        if msa_option == "Don't use MSA 🚫":
            protein_entry["pairedMsa"] = ""  # Explicitly set to empty string
    if templates_list:
        protein_entry["templates"] = templates_list

    return protein_entry

def handle_rna_entity(i, entity_ids):
    sequence = st.text_area(f"RNA Sequence (Entity {i+1})", key=f"sequence_{i}", help="Enter the RNA sequence.")
    # Modifications
    modifications_list = []
    add_modifications = st.checkbox(f"Add Modifications", key=f"add_modifications_{i}")
    if add_modifications:
        num_modifications = st.number_input(f"Number of Modifications", min_value=1, step=1, key=f"num_modifications_{i}")
        for j in range(int(num_modifications)):
            st.markdown(f"**Modification {j+1}**")
            mod_col1, mod_col2 = st.columns(2)
            with mod_col1:
                mod_type = st.text_input(f"Modification Type (modificationType)", key=f"mod_type_{i}_{j}")
            with mod_col2:
                mod_position = st.number_input(f"Modification Position (basePosition)", min_value=1, step=1, key=f"mod_position_{i}_{j}")
            modifications_list.append({"modificationType": mod_type, "basePosition": mod_position})

    # MSA Options
    msa_option = st.selectbox(f"MSA Option", ["Auto-generate 🛠️", "Don't use MSA 🚫", "Upload MSA 📄"], key=f"msa_option_{i}")
    if msa_option == "Upload MSA 📄":
        unpaired_msa = st.text_area(f"Unpaired MSA", key=f"unpaired_msa_{i}")
    elif msa_option == "Don't use MSA 🚫":
        unpaired_msa = ""
    else:
        unpaired_msa = None  # Auto-generate

    rna_entry = {
        "id": entity_ids if len(entity_ids) > 1 else entity_ids[0],
        "sequence": sequence
    }
    if modifications_list:
        rna_entry["modifications"] = modifications_list
    if unpaired_msa is not None:
        rna_entry["unpairedMsa"] = unpaired_msa

    return rna_entry

def handle_dna_entity(i, entity_ids):
    sequence = st.text_area(f"DNA Sequence (Entity {i+1})", key=f"sequence_{i}", help="Enter the DNA sequence.")
    # Modifications
    modifications_list = []
    add_modifications = st.checkbox(f"Add Modifications", key=f"add_modifications_{i}")
    if add_modifications:
        num_modifications = st.number_input(f"Number of Modifications", min_value=1, step=1, key=f"num_modifications_{i}")
        for j in range(int(num_modifications)):
            st.markdown(f"**Modification {j+1}**")
            mod_col1, mod_col2 = st.columns(2)
            with mod_col1:
                mod_type = st.text_input(f"Modification Type (modificationType)", key=f"mod_type_{i}_{j}")
            with mod_col2:
                mod_position = st.number_input(f"Modification Position (basePosition)", min_value=1, step=1, key=f"mod_position_{i}_{j}")
            modifications_list.append({"modificationType": mod_type, "basePosition": mod_position})

    dna_entry = {
        "id": entity_ids if len(entity_ids) > 1 else entity_ids[0],
        "sequence": sequence
    }
    if modifications_list:
        dna_entry["modifications"] = modifications_list

    return dna_entry

def handle_ligand_entity(i, entity_ids):
    ligand_ids = entity_ids
    ccd_codes = st.text_input(f"CCD Codes (comma-separated)", key=f"ccd_codes_{i}", help="Provide CCD Codes, separated by commas.")
    smiles = st.text_input(f"SMILES String", key=f"smiles_{i}", help="Provide SMILES string of the ligand.")
    if ccd_codes and smiles:
        st.error("Please provide only one of CCD Codes or SMILES String.")
        return None
    elif ccd_codes:
        ccd_codes_list = re.split(r"\s*,\s*", ccd_codes)
        ligand_entry = {
            "id": ligand_ids if len(ligand_ids) > 1 else ligand_ids[0],
            "ccdCodes": ccd_codes_list
        }
        return ligand_entry
    elif smiles:
        ligand_entry = {
            "id": ligand_ids if len(ligand_ids) > 1 else ligand_ids[0],
            "smiles": smiles
        }
        return ligand_entry
    else:
        st.error("Ligand requires either CCD Codes or SMILES String.")
        return None

def handle_bond(b):
    bond_col1, bond_col2 = st.columns(2)
    with bond_col1:
        st.markdown("**First Atom**")
        entity_id1 = st.text_input(f"Entity ID 1", key=f"bond_entity1_{b}")
        residue_id1 = st.number_input(f"Residue ID 1", min_value=1, step=1, key=f"bond_residue1_{b}")
        atom_name1 = st.text_input(f"Atom Name 1", key=f"bond_atom1_{b}")
    with bond_col2:
        st.markdown("**Second Atom**")
        entity_id2 = st.text_input(f"Entity ID 2", key=f"bond_entity2_{b}")
        residue_id2 = st.number_input(f"Residue ID 2", min_value=1, step=1, key=f"bond_residue2_{b}")
        atom_name2 = st.text_input(f"Atom Name 2", key=f"bond_atom2_{b}")

    if not (entity_id1 and atom_name1 and entity_id2 and atom_name2):
        st.error("All fields are required for defining a bond.")
        return None

    return [
        [entity_id1, residue_id1, atom_name1],
        [entity_id2, residue_id2, atom_name2]
    ]

if __name__ == "__main__":
    main()