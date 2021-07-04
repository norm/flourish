from flourish.dirtrie import DirTrie, TrieNode


class TestDirTrie:
    @classmethod
    def setup_class(self):
        self.uploads = [
            '/',
            '/2021/',
            '/2021/06/',
            '/2021/06/29/',
            '/2021/06/29/ostentatious',
            '/2021/06/29/github_activity',
            '/2021/06/28/go-get-her',
            '/2021/01/04/horizon-zero-dawn-chapter-30-glitch',
            '/2021/01/18/nathan-evans-wellerman-family-tree-shantytok-mashupsupercut',
            '/2021/04/05/horizon-zero-dawn-chapter-54-sacrifice',
            '/code/',
            '/code/repository/concourse-cron-resource',
            '/code/repository/gifs-cackhanded-net',
            '/code/repository/',
            '/code/repository/marknormanfrancis-com',
            '/2010/07/17/devfort-cohort-4-prioritisation',
            '/2010/07/18/devfort-cohort-4-third-day-of-coding',
            '/2010/07/19/devfort-cohort-4-last-day-of-coding',
            '/tags/repo-gifs-cackhanded-net/',
            '/tags/cheryl-frasier/',
            '/tags/gracie-hart/',
            '/tags/ray-stantz/',
            '/tags/repo-concourse-cron-resource/',
            '/tags/gracie-lou-freebush/',
            '/tags/repo-marknormanfrancis-com/',
            '/tags/miss-congeniality/',
            '/tags/ghostbusters/',
            '/tags/miss-new-jersey/',
            '/tags/miss-rhode-island/',
            '/tags/peter-venkman/',
            '/2020/09/24/horizon-zero-dawn-chapter-1-aloy',
        ]
        self.uploads_collapsed_tags = [
            '/',
            '/2021/',
            '/2021/06/',
            '/2021/06/29/',
            '/2021/06/29/ostentatious',
            '/2021/06/29/github_activity',
            '/2021/06/28/go-get-her',
            '/2021/01/04/horizon-zero-dawn-chapter-30-glitch',
            '/2021/01/18/nathan-evans-wellerman-family-tree-shantytok-mashupsupercut',
            '/2021/04/05/horizon-zero-dawn-chapter-54-sacrifice',
            '/code/',
            '/code/repository/concourse-cron-resource',
            '/code/repository/gifs-cackhanded-net',
            '/code/repository/',
            '/code/repository/marknormanfrancis-com',
            '/2010/07/17/devfort-cohort-4-prioritisation',
            '/2010/07/18/devfort-cohort-4-third-day-of-coding',
            '/2010/07/19/devfort-cohort-4-last-day-of-coding',
            '/tags/*',
            '/2020/09/24/horizon-zero-dawn-chapter-1-aloy',
        ]

    def insert_bulk(self, trie):
        for upload in self.uploads:
            trie.insert(upload)

    def test_trie_size(self):
        trie = DirTrie()
        assert trie.size() == 1
        assert trie.published_count() == 0
        trie.insert('/2021/06/28/go-get-her')
        assert trie.size() == 5
        assert trie.published_count() == 1
        trie.insert('/2021/06/28/go-get-her')
        assert trie.size() == 5
        assert trie.published_count() == 1

    def test_trie_find(self):
        trie = DirTrie()
        trie.insert('/2021/06/28/go-get-her')
        trie.insert('/2021/06/29/github_activity')

        assert trie.find('/nope') == None

        ggh = trie.find('/2021/06/28/go-get-her')
        assert type(ggh) == TrieNode
        assert ggh.published == True
        assert ggh.children == {}

        year = trie.find('/2021/')
        assert type(year) == TrieNode
        assert year.published == False
        assert [k for k in year.children.keys()] == ['/2021/06/']

    def test_trie_collapse_to_all(self):
        trie = DirTrie()
        self.insert_bulk(trie)
        assert trie.published_count() == 31

        assert sorted(trie.collapse(31)) == sorted(self.uploads)
        assert sorted(trie.collapse(30)) == sorted(self.uploads_collapsed_tags)
        assert trie.collapse(1) == ['/*']

        for i in range(32, 0, -1):
            assert len(trie.collapse(i)) <= i
