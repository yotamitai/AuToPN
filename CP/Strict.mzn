%               Input
int: num_timepoints;
set of int: timepoints = 1..num_timepoints;
array [1..num_timepoints, 1..num_timepoints] of bool: compatible;
array [1..num_timepoints] of int: original_min = timepoints;

%              Output
array [timepoints, timepoints] of var bool: merge;
array [timepoints] of var 1..num_timepoints: minimum;

% output[show(sum(t1 in timepoints) (if minimum[t1] != original_min[t1] then 1 else 0 endif))];

%           Constraints
% setting the original minimum
constraint forall(t1 in timepoints)(minimum[t1]<=original_min[t1]);
% a merge implies the symetric merge
constraint forall(t1,t2 in timepoints)(merge[t1,t2] <-> merge[t2,t1]);
% a merge implies compatibility
constraint forall(t1,t2 in timepoints)(merge[t1,t2] -> compatible[t1,t2]);
%set the diagonal to true
constraint forall(t1 in timepoints)(merge[t1,t1] = true);
% if merge exists then nodes share same minimum node
constraint forall(t1 in timepoints)(minimum[t1] != original_min[t1] -> merge[t1,minimum[t1]]);
constraint forall(t1,t2 in timepoints)(merge[t1,t2] -> minimum[t1] = min(minimum[t1],minimum[t2]));


% Strict
% if t1,t2 and t1,t3 are merges, then it implies that t2,t3 are compatible 
constraint forall(t1,t2,t3 in timepoints)( (merge[t1,t2] /\ merge[t1,t3])->(compatible[t1,t2]/\compatible[t1,t3]/\compatible[t2,t3]) );


%           Objective
% solve maximize (sum(t1,t2 in timepoints) (merge[t1,t2]));
solve maximize (sum(t1 in timepoints) (if minimum[t1] != original_min[t1] then 1 else 0 endif));
                                                                    
