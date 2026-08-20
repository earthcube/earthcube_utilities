"""The graph managers can actually be constructed.

Offline and deliberately narrow: no namespace is created, nothing is loaded,
nothing talks to a server. It exists because `rebuildNamespaceFromReleases` was
decorated @abstractmethod while having a full body and no subclass overriding
it, which made every manager uninstantiable -- a TypeError raised at the
constructor, in production, from an asset that had never exercised this path.
Anything with an @abstractmethod nobody implements fails here rather than there.
"""
import inspect
import unittest

from ec.graph.manageGraph import ManageBlazegraph, ManageGraph, ManageGraphdb

URL = "http://localhost:9999/blazegraph"


class ManageGraphInstantiationTestCase(unittest.TestCase):

    def test_blazegraph_can_be_constructed(self):
        bg = ManageBlazegraph(URL, "test_namespace")

        self.assertEqual("test_namespace", bg.namespace)

    def test_graphdb_can_be_constructed(self):
        ManageGraphdb(URL, "test_namespace")

    def test_rebuild_from_releases_is_inherited_not_abstract(self):
        """It is a template method over the abstract ones, so subclasses get it
        for free; if it goes back to being abstract they stop constructing."""
        self.assertFalse(
            getattr(ManageGraph.rebuildNamespaceFromReleases,
                    "__isabstractmethod__", False))
        self.assertEqual(ManageGraph.rebuildNamespaceFromReleases,
                         ManageBlazegraph.rebuildNamespaceFromReleases)

    def test_every_abstract_method_is_implemented_by_blazegraph_and_graphdb(self):
        """The general form of the bug: an abstract method nobody overrides."""
        for cls in (ManageBlazegraph, ManageGraphdb):
            with self.subTest(cls=cls.__name__):
                self.assertEqual(
                    frozenset(), cls.__abstractmethods__,
                    f"{cls.__name__} cannot be instantiated; unimplemented: "
                    f"{sorted(cls.__abstractmethods__)}")

    def test_abstract_methods_are_declared_on_the_base(self):
        """Guards the inverse mistake -- a stub that silently stopped being
        required."""
        abstract = ManageGraph.__abstractmethods__

        self.assertIn("createNamespace", abstract)
        self.assertIn("deleteNamespace", abstract)
        self.assertIn("loadReleaseFromUrl", abstract)
        self.assertNotIn("rebuildNamespaceFromReleases", abstract)


if __name__ == '__main__':
    unittest.main()
