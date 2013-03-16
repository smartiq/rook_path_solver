#!/usr/bin/env python
##########################################################################
# Script to calulate solutions to Rook problem
#
# Copyright (C) 2013  Barry Grussling
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; version
# 2 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301, USA.
#
# Inspired by http://www.kchodorow.com/blog/2013/03/04/the-google-interviews/
# and http://www.iwriteiam.nl/Crook_path.html
#
# This script solves the basic problem of:
#
# Suppose you are on a Cartesian coordinate system. Find all paths from (0,0)
# to (m,n) that only go through each point once. For example, if you were
# given m=2, n=2 you'd have the following:
#
#     . . . (2,2)
#
#     . . .
#
#     . . .
# (0,0)
#
# One possible path would be:
#     ._. . (2,2)
#     | | |
#     . ._.
#     |
#     . . .
# (0,0)
#
# What are all the paths and how many are there?

import sys
import logging

class grid(object):
   """This class stores a particular solution"""
   def __init__(self,m,n,connections):
      # Store off variables
      self.m = m
      self.n = n
      self.connections = connections
      self.display_len = len(str((self.m + 1) * (self.n + 1)))

   def print_layout(self):
      """This method "pretty prints" the grid.

         It tries to handle the various cases of different number
         widths for the point labels

         Note that we lay stuff out in a grid like

         . . . ------------> m direction

         . . .

         . . .

         |
         V
         n direction

         """
      if "-p" in sys.argv:
         print self.connections

      # Note we go based off cell ID rather than rows and columns per se.
      for row_start in range(0, (self.m + 1) * (self.n + 1), self.m + 1):
         sys.stdout.write('{0: >{width}}'.format(row_start,
                                                 width=self.display_len))

         # Horizonal Lines
         for cell_number in range(row_start, row_start + self.m):
            if (cell_number, cell_number + 1) in self.connections or \
               (cell_number + 1, cell_number) in self.connections:
               sys.stdout.write('__{0: >{width}}'.format(cell_number+1,
                                                     width = self.display_len))
            else:
               sys.stdout.write('  {0: >{width}}'.format(cell_number+1,
                                                     width = self.display_len))
         sys.stdout.write('\n')

         # Vertical Lines
         for cell_number in range(row_start, row_start + self.m + 1):
            # Allow for connections in either (src,dst) or (dst,src) format
            if (cell_number, cell_number + self.m + 1) in self.connections or \
               (cell_number + self.m + 1, cell_number) in self.connections:
               sys.stdout.write('{0: >{width}}'.format('|',
                                width=self.display_len) + \
                                ' ' * 2)
            else:
               sys.stdout.write('{0: >{width}}'.format (' ',
                                width = self.display_len) + \
                                ' ' * 2)
         sys.stdout.write('\n')

class grid_set(object):
   """This class is a container for various grids.  The
      constructor generates all the grid enumerations, stores
      them, and can display some summary information"""

   # "Enumeration" of possible move directions
   DIR_DOWN = 'd'
   DIR_RIGHT = 'r'
   DIR_UP = 'u'
   DIR_LEFT = 'l'

   def __init__(self,m,n):
      self.m = m
      self.n = n

      # Do the work of actually building the solutions
      self.enumerated = self.enumerate_grids()

   def print_solutions(self):
      """Print out every grid in our solutions"""
      for grid in self.enumerated:
         grid.print_layout()
         print ""

   def print_summary(self):
      """Simple summary"""
      print "Found:", len(self.enumerated), "solutions"

   def allowed_transition(self,
                          current_location,
                          desired_location,
                          seen_nodes):
      """Called to see if current_location can move to desired_location
         based on seen_nodes and structure of graph"""
      if desired_location in seen_nodes:
         logging.debug("Can't move to visited nodes")
         return False

      if desired_location < 0:
         # This handles moving from top row up and left from 0,0
         logging.debug("Can't move to cell before beginning")
         return False

      if desired_location >= (self.m + 1) * (self.n + 1):
         # This handles moving bottom row down and right from m,n
         logging.debug("Can't move to cell past end")
         return False

      # Now handle the case of moving left from left col and right from right
      # column
      logging.debug("abs: %d", abs(current_location - desired_location))
      if abs(current_location - desired_location) == 1:
         # We are moving right or left.  Make sure we stay in the same row.
         current_row = current_location / (self.m + 1)
         desired_row = desired_location / (self.m + 1)
         logging.debug("Current Row: %d", current_row)
         logging.debug("Desired Row: %d", desired_row)
         if (desired_row != current_row):
            logging.debug("Can't move across rows")
            return False

      # Must be okay
      logging.debug("This is an allowed transition")
      return True

   def permutations(self,
                    current_location = 0,
                    desired_direction = None,
                    current_path = None):
      """Recusive method to calculate all valid permutations"""

      # "Unroll" the nodes in our visit list so we have a list of
      # nodes we have been at before
      seen_nodes = [current_location]
      if current_path is not None:
         for (src, dst) in current_path:
            if src not in seen_nodes:
               seen_nodes.append(src)
            if dst not in seen_nodes:
               seen_nodes.append(dst)

      logging.debug("At %s, got here via %s, going %s",
                    current_location,
                    current_path,
                    desired_direction)

      if current_location == (self.m + 1) * (self.n + 1) - 1:
         # We found a path to the corner!
         logging.debug("Found a solution!")
         logging.debug("")
         yield grid(self.m, self.n, current_path)

      elif desired_direction is None:
         # We just reached this node.  Go everywhere.
         logging.debug("Going Everywhere")
         for direction in grid_set.DIR_DOWN, \
                          grid_set.DIR_RIGHT, \
                          grid_set.DIR_UP, \
                          grid_set.DIR_LEFT:
            for perm in  self.permutations(current_location = current_location,
                                           desired_direction = direction,
                                           current_path = current_path):
               yield perm

      else:
         # We need to head in a specific direction
         logging.debug("Going %s", desired_direction)
         if desired_direction == grid_set.DIR_DOWN:
            desired_location = current_location + self.m + 1
         elif desired_direction == grid_set.DIR_RIGHT:
            desired_location = current_location + 1
         elif desired_direction == grid_set.DIR_LEFT:
            desired_location = current_location - 1
         elif desired_direction == grid_set.DIR_UP:
               desired_location = current_location - self.m - 1

         if self.allowed_transition(current_location,
                                    desired_location,
                                    seen_nodes):
            path_to_next = ((current_location, desired_location),)
            if current_path is not None:
               path_to_next = ((current_path) + (path_to_next))
            for perm in self.permutations(current_location = desired_location,
                                          current_path = path_to_next):
               yield perm

   def enumerate_grids(self):
      """Run out and collect all the grids that are solutions"""
      grids = []
      for grid in self.permutations():
         grids.append(grid)
      return grids

if __name__ == '__main__':
   # Yeah yeah.  This could be made better or it could use getopts or
   # something but I don't care right this second :-)
   if len(sys.argv) < 3 or len(sys.argv) > 6:
      print "Usage: {0} [-d] [-s [-p]] <m> <n>".format(sys.argv[0])
      print "       -d Print debug information"
      print "       -s Print solutions"
      print "       -p Print paths with solutions"
      sys.exit(1)

   if "-d" in sys.argv:
      logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

   grid_set = grid_set(int(sys.argv[-2]), int(sys.argv[-1]))
   if "-s" in sys.argv:
      grid_set.print_solutions()
   grid_set.print_summary()
