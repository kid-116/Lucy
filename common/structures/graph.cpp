struct Graph {
  int n;
  vector<vector<pair<int, int>>> adj;

  Graph(int n, const vector<tuple<int, int, int>> &edges,
        bool directed = false) {
    Graph::n = n;
    adj.resize(n);
    for (auto [u, v, w] : edges) {
      adj[u].push_back({v, w});
      if (!directed) {
        adj[v].push_back({u, w});
      }
    }
  }

  v64 run_djikstra(int s) {
    v64 d(n, INT64_MAX);
    set<pair<int, int>> q;

    d[s] = 0;
    q.insert({0, s});

    while (!q.empty()) {
      auto [_, u] = *q.begin();
      q.erase(q.begin());
      for (auto const &[to, len] : adj[u]) {
        if (d[u] + len < d[to]) {
          q.erase({d[to], to});
          d[to] = d[u] + len;
          q.insert({d[to], to});
        }
      }
    }

    return d;
  }
};
