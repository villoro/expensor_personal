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

            # Check that there is a sidebar and a body
            self.driver.find_element_by_id("sidebar")
            self.driver.find_element_by_id("body")


    def _check_one_page(self, page_link, elements):
        """
            Check the existence of some elements in a page

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

        body_elem = ["plot_dash_evol", "plot_dash_l_vs_e", "plot_dash_liq_months"]
        #sidebar_elem = ["slider_dash_rolling_avg"]
        self._check_one_page(c.dash.LINK_DASHBOARD, body_elem) # + sidebar_elem)


    def test_page_evolution(self):
        """ Test the content of page evolution """

        body_elem = ["plot_evol", "radio_evol_type", "drop_evol_categ", "radio_evol_tw"]
        sidebar_elem = ["drop_evol_categ", "radio_evol_tw"]
        self._check_one_page(c.dash.LINK_EVOLUTION, body_elem + sidebar_elem)


    def test_page_comparison(self):
        """ Test the content of page comparison """

        body_elem = ["plot_comp_1", "radio_comp_1", "plot_comp_2", "radio_comp_2"]
        sidebar_elem = ["drop_comp_categ"] #, "slider_comp_rolling_avg"]
        self._check_one_page(c.dash.LINK_COMPARISON, body_elem + sidebar_elem)


    def test_page_heatmaps(self):
        """ Test the content of page heatmaps """

        body_elem = ["plot_heat_i", "plot_heat_e", "plot_heat_distribution"]
        sidebar_elem = ["drop_heat_categ"]
        self._check_one_page(c.dash.LINK_HEATMAPS, body_elem + sidebar_elem)


    def test_page_pies(self):
        """ Test the content of page pies """

        body_elem = ["drop_pie_1"] # "drop_pie_2", "plot_pie_1", "plot_pie_2"
        sidebar_elem = ["drop_pie_categ"]
        self._check_one_page(c.dash.LINK_PIES, body_elem + sidebar_elem)



if __name__ == '__main__':
    unittest.main()
