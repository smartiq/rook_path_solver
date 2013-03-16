Rook Path Solver
================

While reading a blog post at snail in a tutleneck
(http://www.kchodorow.com/blog/2013/03/04/the-google-interviews/), I was
intrigued by the Cartesian Coordinate System problem.  I realized that I
didn't have a very good answer for it, so I decided to write a script to
explore the problem space.

After generating some of the solutions and plugging them into Google
I discovered that this was known as the Rook Path Problem.  Before that
it didn't have a name.  After having the name, I found:
http://www.iwriteiam.nl/Crook_path.html which contains some good information.

Usage
------------------
<pre>
Usage: path_finder.py [-d] [-s [-p]] <m> <n>
    -d Print debug information
    -s Print solutions
    -p Print paths with solutions
</pre>

Example
------------------
<pre>
time python path_finder.py -s 2 2
0  1  2
|        
3  4  5
|        
6__7__8
         

0  1  2
|        
3  4__5
|  |  |  
6__7  8
         

0  1__2
|  |  |  
3  4  5
|  |  |  
6__7  8
         

0  1  2
|        
3__4  5
   |     
6  7__8
         

0  1  2
|        
3__4__5
      |  
6  7  8
         

0  1__2
|  |  |  
3__4  5
      |  
6  7  8
         

0__1  2
   |     
3  4  5
   |     
6  7__8
         

0__1  2
   |     
3  4__5
      |  
6  7  8
         

0__1  2
   |     
3__4  5
|        
6__7__8
         

0__1__2
      |  
3  4  5
      |  
6  7  8
         

0__1__2
      |  
3  4__5
   |     
6  7__8
         

0__1__2
      |  
3__4__5
|        
6__7__8
         

Found: 12 solutions

real    0m0.025s
user    0m0.020s
sys     0m0.004s
</pre>

