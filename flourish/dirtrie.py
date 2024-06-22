import os


class NotPath(Exception):
    pass


class TrieNode:
    def __init__(self, path):
        self.path = path
        self.children = dict()
        self.published = False


class DirTrie:
    """
    A DirTrie is a trie-like structure, splitting paths per directory
    (whereas a class trie builds a character-based tree).

    Its primary purpose is to take a list of generated paths, and collapse
    that list to a smaller number for use in CloudFront invalidation requests.
    Republishing an entire site with >1000 paths (eg the footer changes,
    so the entire site is rebuilt) edges into paid-for invalidation costs.
    Being able to collapse a list into a smaller list of invalidation paths,
    even at the expense of expunging valid paths from the edge cache works
    out cheaper for small traffic sites.
    """
    def __init__(self):
        self.root = TrieNode('/')

    def split_paths(self, path):
        """
        Turn '/a/b/c' into [/, /a/, /a/b/, /a/b/c] for ease of use.
        """
        if not path.startswith('/'):
            raise NotPath
        paths = [path,]
        while path != '/':
            head, tail = os.path.split(path)
            if tail != '':
                paths.insert(0, os.path.join(head, ''))
            path = head
        return paths

    def insert(self, path):
        """
        Insert a new published path into the trie.
        """
        node = self.root
        paths = self.split_paths(path)
        for path in paths:
            if path == '/':
                continue
            if path not in node.children:
                node.children[path] = TrieNode(path=path)
            node = node.children[path]
        node.published = True

    def size(self, node=None):
        """
        Count the number of nodes below the specified node
        (default: root node).
        """
        if not node:
            node = self.root
        count = 1
        for child in node.children:
            count += self.size(node.children[child])
        return count

    def published_count(self, node=None):
        """
        Count the number of nodes that represent published paths below the
        specied node (default: root).
        """
        if not node:
            node = self.root
        count = 0
        if node.published:
            count = 1
        for child in node.children:
            count += self.published_count(node.children[child])
        return count

    def published_paths(self, node=None):
        """
        Return the list of nodes that represent published paths below
        the specified node (default: root node).
        """
        paths = []
        if node is None:
            node = self.root
        if node.published:
            paths.append(node.path)
        for child in node.children:
            paths.extend(self.published_paths(node.children[child]))
        return paths

    def find(self, path):
        """
        Find the node for a given path, if it exists.
        """
        node = self.root
        paths = self.split_paths(path)
        for path in paths:
            if path == '/':
                continue
            if path not in node.children:
                return None
            node = node.children[path]
        return node

    def collapse(self, max, node=None):
        """
        Reduce the number of published paths to `max` or below for CloudFront
        invalidation. Packs in the subpaths with the smallest number of
        changes first, then the bigger ones. Anything with too many paths is
        returned as '/a/b/*', a wildcard invalidation which can invalidate
        many paths, but is only billed as one path.
        """
        if node is None:
            node = self.root

        if len(self.published_paths(node)) <= max:
            return self.published_paths(node)

        paths = []
        if node.children:
            if len(node.children) > max:
                return ['%s*' % node.path]

            children = [
                x for x in sorted(
                    node.children,
                    key=lambda c: self.published_count(node.children[c]),
                )
            ]
            remains = max - len(children)
            if node.published:
                remains -= 1
            for child in children:
                new_paths = self.collapse(remains + 1, node.children[child])
                paths.extend(new_paths)
                remains -= len(new_paths) - 1

        if node.published:
            paths.append(node.path)

        if max - len(paths) < 0:
            paths = ['%s*' % node.path]

        return paths

    def print_trie(self, node=None, depth=0):
        """
        Print the trie structure, for debugging.
        """
        if node is None:
            node = self.root
        pub_icon = '--'
        if node.published:
            pub_icon = '**'
        print('  '*depth, pub_icon, node.path)
        for child in node.children:
            self.print_trie(node.children[child], depth+1)
