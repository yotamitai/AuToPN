%               Input
int: num_timepoints;
set of int: timepoints = 1..num_timepoints;
array [timepoints, timepoints] of bool: compatible;
array [timepoints] of int: node_plans;
array [1..num_timepoints] of int: original_min = timepoints;
% output[show(node_plans)];

%              Output
array [timepoints, timepoints] of var bool: merge;
array [timepoints] of var 1..num_timepoints: minimum;

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

% this constraint ruins the optimization for some reason
% constraint forall(t1,t2 in timepoints)(merge[t1,t2] -> minimum[t1] = min(minimum[t1],minimum[t2]));


%Loose
%not from same plan
constraint forall(t1,t2 in timepoints where t1 != t2)(merge[t1,t2] -> (node_plans[t1] != node_plans[t2]));
constraint forall(t1,t2,t3 in timepoints  where t1 != t2 /\ t2 != t3 /\ t1 != t3)(merge[t1,t2] /\ merge[t1,t3]-> (node_plans[t2] != node_plans[t3]));
constraint forall(t1,t2 in timepoints where t1 != t2)(minimum[t1] == minimum[t2] -> node_plans[t1] != node_plans[t2] );


solve maximize (sum(t1 in timepoints) (if minimum[t1] != original_min[t1] then 1 else 0 endif));
% solve maximize (sum(t1,t2 in timepoints) (merge[t1,t2]));
