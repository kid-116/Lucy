template <typename T>
long long sum_abs_diff_all_pairs(vector<T> &vec)
{
    sort(all(vec));
    long long tot_sum = accumulate(all(vec), 0ll);
    long long running = 0;
    long long soln = 0;
    for (int i = 0; i < vec.size(); i++)
    {
        T &ele = vec[i];
        soln += (long long)(ele)*i - running;
        soln += (tot_sum - running - ele) - (long long)(ele) * (vec.size() - i - 1);
        running += ele;
    }
    return soln / 2;
};
