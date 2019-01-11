//using namespace std;


int min(int x, int y)
{
  if (x <= y) return x;
  else return y;
}


int minimum(int a, int b, int c)  {return min(min(a, b), c);}



int _levenshtein(int *s, int len_s, int *t, int len_t)
{
	int cost;

  /* base case: empty strings */
  if (len_s == 0) return len_t;
  if (len_t == 0) return len_s;

  /* test if last characters of the strings match */
  if (s[len_s-1] == t[len_t-1])
      cost = 0;
  else
      cost = 1;

  /* return minimum of delete char from s, delete char from t, and delete char from both */
  return minimum(_levenshtein(s, len_s - 1, t, len_t    ) + 1,
                 _levenshtein(s, len_s    , t, len_t - 1) + 1,
                 _levenshtein(s, len_s - 1, t, len_t - 1) + cost);
}




int _wagner_fischer(int *s, int m, int *t, int n)
{
	int d[m+1][n+1];

	for (int i=0; i<=m; i++)
	{
    d[i][0] = i;  // the distance of any first string to an empty second string
  }              // (transforming the string of the first i characters of s into
                 // the empty string requires i deletions)

	for (int j=0; j<=n; j++)
	{
  	d[0][j] = j;  // the distance of any second string to an empty first string
	}


	for (int j=1; j<=n; j++)
  {
		for (int i=1; i<=m; i++)
    {
       if (s[i-1] == t[j-1])
         d[i][j] = d[i-1][j-1];        // no operation required
       else
       {
         d[i][j] = minimum(d[i-1][j] + 1,   // a deletion
                      		d[i][j-1] + 1,   // an insertion
                      		d[i-1][j-1] + 1);// a substitution
       }
    }
  }
 
  return d[m][n];
}















