# ==================================================================================================
#
#    Copyright (c) 2008, Patrick Janssen (patrick@janssen.name)
#
#    This file is part of Eddex.
#
#    Eddex is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Eddex is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Eddex.  If not, see <http://www.gnu.org/licenses/>.
#
# ==================================================================================================
"""
Tasks executed by this evolutionary algorithm.

Houdini needs to have the following libs in python27:
- bson
- pymongo
"""
import sys
import settings as ss

from dexen_libs.moea.executors import (
    initialize, 
    develop,
    evaluate,
    feedback)

def main(task_name):
    #------------------------------------------------------------------------------
    #INITIALIZE TASK
    #------------------------------------------------------------------------------
    if task_name == ss.INITIALIZE:
        if ss.VERBOSE:
            print "Initialize task creating individuals "
        initialize(genotype_meta = ss.genotype_meta, initial_pop_size = ss.POP_SIZE)
    #------------------------------------------------------------------------------
    #DEVELOPMENT TASK
    #------------------------------------------------------------------------------
    elif task_name == ss.DEVELOP:
        if ss.VERBOSE:
            print "Develop task processing individuals "
        from houdini_ea.wrappers import houdini_develop
        develop(func = houdini_develop, 
            hip_file_name = ss.DEVELOP_HIP_FILE_NAME, 
            in_path = ss.DEVELOP_IN_PATH, 
            out_path = ss.DEVELOP_OUT_PATH, 
            animate = ss.DEVELOP_ANIMATE)
    #------------------------------------------------------------------------------
    #EVALUATION TASK 1
    #------------------------------------------------------------------------------
    elif task_name == ss.EVALUATE_AREA:
        if ss.VERBOSE:
            print "Evaluate area task processing individuals "
        from houdini_ea.wrappers import houdini_evaluate
        evaluate(func = houdini_evaluate, score_names = [ss.AREA_SCORE], 
            hip_file_name = ss.EVALUATE_AREA_HIP_FILE_NAME, 
            in_path = ss.EVALUATE_AREA_IN_PATH, 
            out_path = ss.EVALUATE_AREA_OUT_PATH, 
            animate = ss.EVALUATE_AREA_ANIMATE)
    #------------------------------------------------------------------------------    
    #EVALUATION TASK 2
    #------------------------------------------------------------------------------
    elif task_name == ss.EVALUATE_VOLUME:
        if ss.VERBOSE:
            print "Evaluate volume task processing individuals "
        from houdini_ea.wrappers import houdini_evaluate
        evaluate(func = houdini_evaluate, score_names = [ss.VOLUME_SCORE], 
            hip_file_name = ss.EVALUATE_VOLUME_HIP_FILE_NAME, 
            in_path = ss.EVALUATE_VOLUME_IN_PATH, 
            out_path = ss.EVALUATE_VOLUME_OUT_PATH, 
            animate = ss.EVALUATE_VOLUME_ANIMATE)
    #------------------------------------------------------------------------------
    #FEEDBACK
    #------------------------------------------------------------------------------
    elif task_name == ss.FEEDBACK:
        if ss.VERBOSE:
            print "Feedback task processing individuals "
        feedback(
            genotype_meta = ss.genotype_meta,
            scores_meta = ss.scores_meta,
            fitness_type = ss.FITNESS_TYPE, 
            births_select_type = ss.BIRTHS_SELECT_TYPE, 
            deaths_select_type = ss.DEATHS_SELECT_TYPE, 
            num_births = ss.NUM_BIRTHS,  
            num_deaths = ss.NUM_DEATHS,  
            mutation_prob = ss.MUTATION_PROB,  
            crossover_prob = ss.CROSSOVER_PROB)

if __name__ == '__main__':
    try:
        sys.argv[1]
    except NameError:
        print "Missing command line arg; you need to specify the task name."
        raise
    else:
        task_name = sys.argv[1]
        if not task_name in [ss.INITIALIZE, ss.DEVELOP, ss.EVALUATE_AREA, ss.EVALUATE_VOLUME, ss.FEEDBACK]:
            print "The task name is invalid."
            raise
        main(task_name)