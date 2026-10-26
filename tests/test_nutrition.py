"""Domain safeguards for hypothetical calorie models, not clinical validation."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_nutrition import build, round_kcal
from nutrition_models import MODELS, ROWS

class NutritionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles=json.loads((ROOT/'data/nutrition/profiles.json').read_text())
        cls.data=build(cls.profiles)
        cls.rows=cls.data['items']

    def test_every_menu_row_has_explicit_decision_and_unique_identity(self):
        self.assertEqual(set(MODELS),set(range(len(ROWS))))
        self.assertEqual(len({r['id'] for r in self.rows}),len(ROWS))
        self.assertEqual(len(self.rows),533)

    def test_withheld_rows_never_leak_numeric_estimates(self):
        unavailable=[r for r in self.rows if r['status']=='unavailable']
        self.assertEqual(len(unavailable),53)
        for r in unavailable:
            self.assertTrue(r['withheld_reason'])
            self.assertEqual(r['components'],[])
            for k in ('kcal','kcal_low','kcal_high','grade'):
                self.assertIsNone(r[k],r['id'])
            self.assertNotIn('kcal_unrounded',r)

    def test_all_estimates_cautioned_and_arithmetic_replays(self):
        ps=self.profiles['profiles']
        for r in self.rows:
            if r['status']!='modeled':continue
            self.assertEqual(r['grade'],'D')
            self.assertTrue(r['serving'])
            for i in range(3):
                total=sum(c['grams'][i]*ps[c['profile']]['kcal_per_100g']/100 for c in r['components'])
                self.assertAlmostEqual(total,r['kcal_unrounded'][i],places=4,msg=r['id'])
            self.assertLessEqual(r['kcal_low'],r['kcal'])
            self.assertLessEqual(r['kcal'],r['kcal_high'])

    def test_shared_bone_in_steak_is_half_not_two_full_steaks(self):
        r=self.rows[115]
        self.assertIn('Half',r['serving'])
        self.assertEqual(r['components'][0]['grams'],[90,120,155])
        self.assertGreater(r['kcal'],250)
        self.assertLess(r['kcal'],500)
        self.assertNotIn('fries',[c['profile'] for c in r['components']])

    def test_pizza_is_whole_and_sushi_four_pieces(self):
        for i in (10,231,349,351,355):
            self.assertIn('whole individual pizza',self.rows[i]['serving'])
            self.assertGreater(self.rows[i]['kcal'],700)
        for i in range(263,273):
            self.assertIn('Four pieces',self.rows[i]['serving'])
            self.assertEqual(self.rows[i]['components'][0]['grams'][1],90)

    def test_optional_protein_and_selectable_sides_are_not_silently_added(self):
        pad=self.rows[26]
        self.assertIn('optional meat/shrimp excluded',pad['serving'])
        self.assertFalse({'shrimp','chicken','beef'} & {c['profile'] for c in pad['components']})
        for i in (371,372,373,374,387):
            self.assertNotIn('fries',[c['profile'] for c in self.rows[i]['components']])
            self.assertIn('excluded',self.rows[i]['serving'])

    def test_conflicting_cocktails_and_unitemized_buffet_stay_unavailable(self):
        for i in (512,513,515,331,262):self.assertEqual(self.rows[i]['status'],'unavailable')
        dirty=self.rows[511]
        self.assertIn('milk',[c['profile'] for c in dirty['components']])
        self.assertNotIn('cream',[c['profile'] for c in dirty['components']])

    def test_known_profile_identity_prevents_juice_crust_and_raisin_mixups(self):
        p=self.profiles['profiles']
        self.assertEqual(p['pineapplejuice']['description'],'Pineapple juice, 100%')
        self.assertEqual(p['raisins']['description'],'Raisins')
        self.assertIn('thin crust',p['pizza']['description'])
        self.assertEqual(p['conch']['kcal_per_100g'],130)
        self.assertEqual(p['muffin']['description'],'Muffin, English')

    def test_changed_profile_id_is_rejected(self):
        bad=copy.deepcopy(self.profiles)
        bad['profiles']['pizza']['fdc_id']=2708617
        with self.assertRaisesRegex(ValueError,'Profile ID changed'):build(bad)

    def test_rounding_does_not_turn_small_coffees_into_claimed_zero(self):
        self.assertEqual(round_kcal(2.4),0)
        page=(ROOT/'index.html').read_text()
        self.assertIn("n.kcal < 10 ? '&lt;10'",page)
        self.assertEqual(round_kcal(345,'low'),340)
        self.assertEqual(round_kcal(345,'high'),350)

if __name__=='__main__':unittest.main()
