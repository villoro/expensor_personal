""" Tests the dash app works """
import unittest

from test.selenium_utils import open_dash, wait_until_loaded

import src.constants as c

class TestApp(unittest.TestCase):
    """ Tests the dash app works """

    driver = open_dash()

    def test_title(self):
        """ Test that the app is able to load """
        self.assertEqual(c.names.TITLE, self.driver.title)


    def test_pages(self):
        """ Test that is possible to open all pages """

        for page in c.dash.LINKS_ALL:
            self.driver.get(c.dash.LINK_ROOT + page)
            wait_until_loaded(self.driver)

            # Check that there is a body and filters divs
            self.driver.find_element_by_id("body")
            self.driver.find_element_by_id("filters")


    def _check_one_page(self, page_link, elements):
        """
            Check the existence of some elements in a page.

            WARNING: it is not possible to check a slider.

            Args:
                page_link:  relative url to the page
                elements:   what to look for
        """

        self.driver.get(c.dash.LINK_ROOT + page_link)
        wait_until_loaded(self.driver)

        # Check that there is a sidebar and a body
        for elem in elements:
            self.driver.find_element_by_id(elem)


    def test_page_dashboard(self):
        """ Test the content of page heatmaps """

        body_elem = [
            "plot_dash_evol", "plot_dash_total_worth", "plot_dash_l_vs_e", "plot_dash_liq_months"
        ]
        sidebar_elem = ["input_time_average"]
        self._check_one_page(c.dash.LINK_DASHBOARD, body_elem + sidebar_elem)


    def test_page_evolution(self):
        """ Test the content of page evolution """

        body_elem = ["plot_evol", "plot_evo_detail", "radio_evol_type"]
        sidebar_elem = ["drop_categories", "input_time_average", "radio_timewindow"]
        self._check_one_page(c.dash.LINK_EVOLUTION, body_elem + sidebar_elem)


    def test_page_comparison(self):
        """ Test the content of page comparison """

        body_elem = ["plot_comp_1", "radio_comp_1", "plot_comp_2", "radio_comp_2"]
        sidebar_elem = ["drop_categories", "input_time_average"]
        self._check_one_page(c.dash.LINK_COMPARISON, body_elem + sidebar_elem)


    def test_page_heatmaps(self):
        """ Test the content of page heatmaps """

        body_elem = ["plot_heat_i", "plot_heat_e", "plot_heat_distribution"]
        sidebar_elem = ["drop_categories"]
        self._check_one_page(c.dash.LINK_HEATMAPS, body_elem + sidebar_elem)


    def test_page_pies(self):
        """ Test the content of page pies """

        types = [c.names.INCOMES, c.names.EXPENSES]
        body_elem = ["plot_pie_{}_{}".format(i, x) for i in range(2) for x in types]
        body_elem += ["drop_pie_0", "drop_pie_1"]

        sidebar_elem = ["drop_categories"]
        self._check_one_page(c.dash.LINK_PIES, body_elem + sidebar_elem)


    def test_page_liquid(self):
        """ Test the content of page liquid """

        body_elem = ["plot_liquid_evo", "plot_liquid_vs_expenses", "plot_liquid_months"]
        sidebar_elem = ["input_time_average"]
        self._check_one_page(c.dash.LINK_LIQUID, body_elem + sidebar_elem)


    def test_page_investments(self):
        """ Test the content of page investments """

        body_elem = ["plot_invest_detail", "radio_invest", "plot_invest_total_worth"]
        sidebar_elem = ["input_time_average"]
        self._check_one_page(c.dash.LINK_INVESTMENTS, body_elem + sidebar_elem)



if __name__ == '__main__':
    unittest.main()
