"""Moss-files reading toools."""


from pandas.core.api import DataFrame

from bramm_data_analysis.loaders.reading._base import BaseReader
from bramm_data_analysis.loaders.reading.excel_utils import ExcelReader


class MossReader(BaseReader):

    """Moss File Readers."""

    merge_sites_with_samples_on = "site_code"
    merge_sites_samples_with_values_on = "sample_code"

    def load_sites(self) -> DataFrame:
        """Load data sites.

        Returns
        -------
        DataFrame
            Sites DataFrame.
        """
        column_mapping = {
            "Code_site_2021": "site_code",
            "CD_INSEE": "site_insee_code",
            "CD_département": "department_code",
            "Lat_deg_decim": "latitude",
            "Long_deg_decim": "longitude",
            "LambertII_X(m)": "x_lambert",
            "LambertII_Y(m)": "y_lambert",
            "Altitude(m)": "altitude",
            "Date_récolte": "date",
            "Conditions_météo": "weather",
            "Nature_strate_arborée": "tree_layer",
            "Nature_strate_arborée_complément": "tree_layer_complement",
            "Recouvrement_strate_arborée": "tree_cover",
        }
        sheet_name = "Sites"
        return ExcelReader(
            column_name_mapping=column_mapping,
            sheet_name=sheet_name,
        ).load(data_path=self.data_path)

    def load_samples(self) -> DataFrame:
        """Load data samples.

        Returns
        -------
        DataFrame
            Sites DataFrame.
        """
        column_mapping = {
            "Code_site_2021": "site_code",
            "Code_echantillon_2021": "sample_code",
            "BRAMM_échantillons hors EC": "sample_outside_complementary_study",
            "BRAMM_échantillons envoyés à l'Europe": "sample_send_europe",
            "EC_Comparaison entre 3 espèces": "cs_3_species_comparison",
            "EC_Comparaison entre Pp & Hc": "cs_2_species_comparison",
            "EC_Repetition_prelevement": "cs_repeated_sampling",
            "EC_Repetition_analyse": "cs_repeated_analysis",
            "Espèce_prélevée": "species",
            "Nb_tapis prélevés": "samples_nb",
            "Nb_tapis prélevés_sous fougères": "fern_samples_nb",
            "Nb_tapis prélevés_sous strate arbustive": "tree_samples_nb",
            "Nb_tapis prélevés_sous strate herbacée": "herb_samples_nb",
            "Nb_tapis prélevés_ sur litière": "litter_samples_nb",
            "Nb_tapis prélevés_ sur humus": "humus_samples_nb",
            "Nb_tapis prélevés_ sur terre": "soi_samples_nb",
            "Nb_tapis prélevés_ sur sable": "sand_samples_nb",
            'Nb_tapis prélevés_pour Hc_ sur souche "dure" (conifères)': "hard_strain_coniferous_samples_nb",  # noqa: E501
            'Nb_tapis prélevés_pour Hc_ sur souche "dure" (feuillus)': "hard_strain_hardwood_samples_nb",  # noqa: E501
            'Nb_tapis prélevés_pour Hc_ sur souche "dure" (inconnu)': "hard_strain_unknown_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur souche en décomposition (conifère": "decomposed_strain_coniferous_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur souche en décomposition (feuillus": "decomposed_strain_hardwood_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur souche en décomposition (inconnu)": "decomposed_strain_unknown_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur BM avec écorce (conifères)": "bark_coniferous_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur BM avec écorce (feuillus)": "bark_hardwood_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur BM avec écorce (inconnu)": "bark_unknown_samples_nb",  # noqa: E501
            'Nb_tapis prélevés_pour Hc_ sur BM "dur" (conifères)': "hard_coniferous_samples_nb",  # noqa: E501
            'Nb_tapis prélevés_pour Hc_ sur BM "dur" (feuillus)': "hard_hardwood_samples_nb",  # noqa: E501
            'Nb_tapis prélevés_pour Hc_ sur BM "dur" (inconnu)': "hard_unknown_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur BM en décomposition (conifères)": "decomposed_coniferous_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur BM en décomposition (feuillus)": "decomposed_hardwood_samples_nb",  # noqa: E501
            "Nb_tapis prélevés_pour Hc_ sur BM en décomposition (inconnu)": "decomposed_unknown_samples_nb",  # noqa: E501
            "Taille_du_brin": "strand_size",
            "Particules de poussière visibles": "visible_dust_particles",
            "Particules de pollen visibles": "visible_pollen_particles",
        }
        sheet_name = "Echantillons"
        return ExcelReader(
            column_name_mapping=column_mapping,
            sheet_name=sheet_name,
        ).load(data_path=self.data_path)

    def load_values(self) -> DataFrame:
        """Load data values.

        Returns
        -------
        DataFrame
            Sites DataFrame.
        """
        column_mapping = {
            "Code_echantillon_2021": "sample_code",
            "Type_minéralisation": "mineral_type",
            "Al_µg/g_103°C": "aluminium",
            "Al_incert_µg/g_103°C": "aluminium_incertitude",
            "As_µg/g_103°C": "arsenic",
            "As_incert_µg/g_103°C": "arsenic_incertitude",
            "Ca_µg/g_103°C": "calcium",
            "Ca_incert_µg/g_103°C": "calcium_incertitude",
            "Cd_µg/g_103°C": "cadmium",
            "Cd_incert_µg/g_103°C": "cadmium_incertitude",
            "Co_µg/g_103°C": "cobalt",
            "Co_incert_µg/g_103°C": "cobalt_incertitude",
            "Cr_µg/g_103°C": "chromium",
            "Cr_incert_µg/g_103°C": "chromium_incertitude",
            "Cu_µg/g_103°C": "copper",
            "Cu_incert_µg/g_103°C": "copper_incertitude",
            "Fe_µg/g_103°C": "iron",
            "Fe_incert_µg/g_103°C": "iron_incertitude",
            "Hg_µg/g_103°C": "mercury",
            "Hg_incert_µg/g_103°C": "mercury_incertitude",
            "N_mg/g_103°C": "nitrogen",
            "N_incert_mg/g_103°C": "nitrogen_incertitude",
            "Na_µg/g_103°C": "sodium",
            "Na_incert_µg/g_103°C": "sodium_incertitude",
            "Ni_µg/g_103°C": "nickel",
            "Ni_incert_µg/g_103°C": "nickel_incertitude",
            "Pb_µg/g_103°C": "lead",
            "Pb_incert_µg/g_103°C": "lead_incertitude",
            "Pd_µg/g_103°C": "palladium",
            "Pt_µg/g_103°C": "platinium",
            "Rh_µg/g_103°C": "rhodium",
            "S_µg/g_103°C": "sulfur",
            "S_incert_µg/g_103°C": "sulfur_incertitude",
            "Sb_µg/g_103°C": "antimony",
            "Sr_µg/g_103°C": "strontium",
            "V_µg/g_103°C": "vanadium",
            "Zn_µg/g_103°C": "zinc",
            "Zn_incert_µg/g_103°C": "zinc_incertitude",
        }
        sheet_name = "Valeurs"
        skiprows = [1]
        return ExcelReader(
            column_name_mapping=column_mapping,
            sheet_name=sheet_name,
            skiprows=skiprows,
        ).load(data_path=self.data_path)

    def retrieve(self) -> DataFrame:
        """Retrieve Data from file.

        Returns
        -------
        DataFrame
            Merged DataFrame.
        """
        sites_data = self.load_sites()
        samples_data = self.load_samples()
        values_data = self.load_values()

        sites_with_samples = sites_data.merge(
            right=samples_data,
            on=self.merge_sites_with_samples_on,
        )
        return sites_with_samples.merge(
            right=values_data,
            on=self.merge_sites_samples_with_values_on,
        )
