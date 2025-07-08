import unittest
from functions.reconcile_accounts import reconcile_accounts


class TestReconcileAccounts(unittest.TestCase):

    def clone(self, t_list):
        """Faz cópia para evitar efeitos colaterais nos testes"""
        return [t[:] for t in t_list]

    def test_basic_reconciliation(self):
        t1 = [
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
            ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares'],
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
        ]
        t2 = [
            ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares'],
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
        ]

        reconciled1, reconciled2 = reconcile_accounts(self.clone(t1), self.clone(t2))

        self.assertEqual(reconciled1, [
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket', 'MISSING'],
            ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares', 'FOUND'],
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
        ])

        self.assertEqual(reconciled2, [
            ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares', 'FOUND'],
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
        ])

    def test_duplicate_transactions(self):
        t1 = [
            ['2020-12-05', 'Tecnologia', '16.00', 'Bitbucket'],
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
        ]
        t2 = [
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
        ]

        reconciled1, reconciled2 = reconcile_accounts(self.clone(t1), self.clone(t2))

        self.assertEqual(reconciled1, [
            ['2020-12-05', 'Tecnologia', '16.00', 'Bitbucket', 'MISSING'],
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket', 'FOUND'],
        ])

        self.assertEqual(reconciled2, [
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket', 'FOUND'],
        ])

    def test_same_key_different_date(self):
        t1 = [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
        ]
        t2 = [
            ['2020-12-04', 'Tecnologia', '50.00', 'AWS'],
        ]

        reconciled1, reconciled2 = reconcile_accounts(self.clone(t1), self.clone(t2))

        self.assertEqual(reconciled1, [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
        ])
        self.assertEqual(reconciled2, [
            ['2020-12-04', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
        ])

    def test_order_preserved(self):
        t1 = [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
            ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares'],
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
        ]
        t2 = [
            ['2020-12-04', 'Tecnologia', '16.00', 'Bitbucket'],
            ['2020-12-04', 'Jurídico', '60.00', 'LinkSquares'],
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
        ]

        reconciled1, _ = reconcile_accounts(self.clone(t1), self.clone(t2))

        # Confirma que a ordem é igual à original
        self.assertEqual([t[:4] for t in reconciled1], t1)

    def test_same_key_different_date(self):
        t1 = [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
            ['2020-12-06', 'Tecnologia', '50.00', 'AWS'],
            ['2020-12-07', 'Tecnologia', '50.00', 'AWS'],
        ]
        t2 = [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS'],
            ['2020-12-06', 'Tecnologia', '50.00', 'AWS'],
            ['2020-12-07', 'Tecnologia', '40.00', 'AWS'],
        ]

        reconciled1, reconciled2 = reconcile_accounts(self.clone(t1), self.clone(t2))

        self.assertEqual(reconciled1, [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
            ['2020-12-06', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
            ['2020-12-07', 'Tecnologia', '50.00', 'AWS', 'MISSING'],
        ])

        self.assertEqual(reconciled2, [
            ['2020-12-05', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
            ['2020-12-06', 'Tecnologia', '50.00', 'AWS', 'FOUND'],
            ['2020-12-07', 'Tecnologia', '40.00', 'AWS', 'MISSING'],
        ])

    def test_all_missing(self):
        t1 = [
            ['2020-12-04', 'RH', '30.00', 'TEST1'],
        ]
        t2 = [
            ['2020-12-04', 'Financeiro', '99.00', 'TEST2'],
        ]

        reconciled1, reconciled2 = reconcile_accounts(self.clone(t1), self.clone(t2))

        self.assertEqual(reconciled1[0][-1], 'MISSING')
        self.assertEqual(reconciled2[0][-1], 'MISSING')

    def test_empty_list(self):
        reconciled1, reconciled2 = reconcile_accounts([], [])
        self.assertEqual([], reconciled1)
        self.assertEqual([], reconciled2)


if __name__ == '__main__':
    unittest.main()
