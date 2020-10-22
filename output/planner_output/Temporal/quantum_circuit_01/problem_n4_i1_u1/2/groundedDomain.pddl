(define (domain quantum-gate)
	(:requirements :strips :typing :durative-actions :negative-preconditions)

	(:predicates
		(located_at_1_q1)
		(located_at_1_q2)
		(located_at_1_q3)
		(located_at_1_q4)
		(located_at_2_q1)
		(located_at_2_q2)
		(located_at_2_q3)
		(located_at_2_q4)
		(located_at_3_q1)
		(located_at_3_q2)
		(located_at_3_q3)
		(located_at_3_q4)
		(located_at_4_q1)
		(located_at_4_q2)
		(located_at_4_q3)
		(located_at_4_q4)
		(NOT_U_GOAL_q1_q1)
		(NOT_U_GOAL_q2_q1)
		(NOT_U_GOAL_q3_q1)
		(NOT_U_GOAL_q4_q1)
		(NOT_U_GOAL_q1_q2)
		(NOT_U_GOAL_q2_q2)
		(NOT_U_GOAL_q3_q2)
		(NOT_U_GOAL_q4_q2)
		(NOT_U_GOAL_q1_q3)
		(NOT_U_GOAL_q2_q3)
		(NOT_U_GOAL_q3_q3)
		(NOT_U_GOAL_q4_q3)
		(NOT_U_GOAL_q1_q4)
		(NOT_U_GOAL_q2_q4)
		(NOT_U_GOAL_q3_q4)
		(NOT_U_GOAL_q4_q4)
		(U_GOAL_q1_q1)
		(U_GOAL_q2_q1)
		(U_GOAL_q3_q1)
		(U_GOAL_q4_q1)
		(U_GOAL_q1_q2)
		(U_GOAL_q2_q2)
		(U_GOAL_q3_q2)
		(U_GOAL_q4_q2)
		(U_GOAL_q1_q3)
		(U_GOAL_q2_q3)
		(U_GOAL_q3_q3)
		(U_GOAL_q4_q3)
		(U_GOAL_q1_q4)
		(U_GOAL_q2_q4)
		(U_GOAL_q3_q4)
		(U_GOAL_q4_q4)
	)


	(:functions
	)

	(:durative-action U_GOAL_action_1_2--q1--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q1_q1))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q1_q1))
			(at end (U_GOAL_q1_q1))
		)
	)

	(:durative-action U_GOAL_action_1_2--q1--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q1_q2))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q1_q2))
			(at end (U_GOAL_q2_q1))
		)
	)

	(:durative-action U_GOAL_action_1_2--q1--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q1_q3))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q1_q3))
			(at end (U_GOAL_q3_q1))
		)
	)

	(:durative-action U_GOAL_action_1_2--q1--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q1_q4))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q1_q4))
			(at end (U_GOAL_q4_q1))
		)
	)

	(:durative-action U_GOAL_action_1_2--q2--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q2_q1))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q2_q1))
			(at end (U_GOAL_q1_q2))
		)
	)

	(:durative-action U_GOAL_action_1_2--q2--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q2_q2))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q2_q2))
			(at end (U_GOAL_q2_q2))
		)
	)

	(:durative-action U_GOAL_action_1_2--q2--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q2_q3))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q2_q3))
			(at end (U_GOAL_q3_q2))
		)
	)

	(:durative-action U_GOAL_action_1_2--q2--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q2_q4))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q2_q4))
			(at end (U_GOAL_q4_q2))
		)
	)

	(:durative-action U_GOAL_action_1_2--q3--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q3_q1))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q3_q1))
			(at end (U_GOAL_q1_q3))
		)
	)

	(:durative-action U_GOAL_action_1_2--q3--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q3_q2))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q3_q2))
			(at end (U_GOAL_q2_q3))
		)
	)

	(:durative-action U_GOAL_action_1_2--q3--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q3_q3))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q3_q3))
			(at end (U_GOAL_q3_q3))
		)
	)

	(:durative-action U_GOAL_action_1_2--q3--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q3_q4))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q3_q4))
			(at end (U_GOAL_q4_q3))
		)
	)

	(:durative-action U_GOAL_action_1_2--q4--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q4_q1))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q4_q1))
			(at end (U_GOAL_q1_q4))
		)
	)

	(:durative-action U_GOAL_action_1_2--q4--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q4_q2))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q4_q2))
			(at end (U_GOAL_q2_q4))
		)
	)

	(:durative-action U_GOAL_action_1_2--q4--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q4_q3))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q4_q3))
			(at end (U_GOAL_q3_q4))
		)
	)

	(:durative-action U_GOAL_action_1_2--q4--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q4_q4))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q4_q4))
			(at end (U_GOAL_q4_q4))
		)
	)

	(:durative-action U_GOAL_action_1_3--q1--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q1_q1))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q1_q1))
			(at end (U_GOAL_q1_q1))
		)
	)

	(:durative-action U_GOAL_action_1_3--q1--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q1_q2))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q1_q2))
			(at end (U_GOAL_q2_q1))
		)
	)

	(:durative-action U_GOAL_action_1_3--q1--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q1_q3))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q1_q3))
			(at end (U_GOAL_q3_q1))
		)
	)

	(:durative-action U_GOAL_action_1_3--q1--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q1_q4))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q1_q4))
			(at end (U_GOAL_q4_q1))
		)
	)

	(:durative-action U_GOAL_action_1_3--q2--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q2_q1))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q2_q1))
			(at end (U_GOAL_q1_q2))
		)
	)

	(:durative-action U_GOAL_action_1_3--q2--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q2_q2))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q2_q2))
			(at end (U_GOAL_q2_q2))
		)
	)

	(:durative-action U_GOAL_action_1_3--q2--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q2_q3))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q2_q3))
			(at end (U_GOAL_q3_q2))
		)
	)

	(:durative-action U_GOAL_action_1_3--q2--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q2_q4))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q2_q4))
			(at end (U_GOAL_q4_q2))
		)
	)

	(:durative-action U_GOAL_action_1_3--q3--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q3_q1))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q3_q1))
			(at end (U_GOAL_q1_q3))
		)
	)

	(:durative-action U_GOAL_action_1_3--q3--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q3_q2))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q3_q2))
			(at end (U_GOAL_q2_q3))
		)
	)

	(:durative-action U_GOAL_action_1_3--q3--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q3_q3))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q3_q3))
			(at end (U_GOAL_q3_q3))
		)
	)

	(:durative-action U_GOAL_action_1_3--q3--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q3_q4))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q3_q4))
			(at end (U_GOAL_q4_q3))
		)
	)

	(:durative-action U_GOAL_action_1_3--q4--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q4_q1))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q4_q1))
			(at end (U_GOAL_q1_q4))
		)
	)

	(:durative-action U_GOAL_action_1_3--q4--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q4_q2))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q4_q2))
			(at end (U_GOAL_q2_q4))
		)
	)

	(:durative-action U_GOAL_action_1_3--q4--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q4_q3))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q4_q3))
			(at end (U_GOAL_q3_q4))
		)
	)

	(:durative-action U_GOAL_action_1_3--q4--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q4_q4))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q4_q4))
			(at end (U_GOAL_q4_q4))
		)
	)

	(:durative-action U_GOAL_action_4_2--q1--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q1_q1))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q1_q1))
			(at end (U_GOAL_q1_q1))
		)
	)

	(:durative-action U_GOAL_action_4_2--q1--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q1_q2))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q1_q2))
			(at end (U_GOAL_q2_q1))
		)
	)

	(:durative-action U_GOAL_action_4_2--q1--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q1_q3))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q1_q3))
			(at end (U_GOAL_q3_q1))
		)
	)

	(:durative-action U_GOAL_action_4_2--q1--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q1_q4))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q1_q4))
			(at end (U_GOAL_q4_q1))
		)
	)

	(:durative-action U_GOAL_action_4_2--q2--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q2_q1))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q2_q1))
			(at end (U_GOAL_q1_q2))
		)
	)

	(:durative-action U_GOAL_action_4_2--q2--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q2_q2))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q2_q2))
			(at end (U_GOAL_q2_q2))
		)
	)

	(:durative-action U_GOAL_action_4_2--q2--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q2_q3))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q2_q3))
			(at end (U_GOAL_q3_q2))
		)
	)

	(:durative-action U_GOAL_action_4_2--q2--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q2_q4))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q2_q4))
			(at end (U_GOAL_q4_q2))
		)
	)

	(:durative-action U_GOAL_action_4_2--q3--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q3_q1))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q3_q1))
			(at end (U_GOAL_q1_q3))
		)
	)

	(:durative-action U_GOAL_action_4_2--q3--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q3_q2))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q3_q2))
			(at end (U_GOAL_q2_q3))
		)
	)

	(:durative-action U_GOAL_action_4_2--q3--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q3_q3))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q3_q3))
			(at end (U_GOAL_q3_q3))
		)
	)

	(:durative-action U_GOAL_action_4_2--q3--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q3_q4))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q3_q4))
			(at end (U_GOAL_q4_q3))
		)
	)

	(:durative-action U_GOAL_action_4_2--q4--q1
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q1))
			(at start (NOT_U_GOAL_q4_q1))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q1)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q1))
			(at end (U_GOAL_q4_q1))
			(at end (U_GOAL_q1_q4))
		)
	)

	(:durative-action U_GOAL_action_4_2--q4--q2
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q2))
			(at start (NOT_U_GOAL_q4_q2))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q2)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q2))
			(at end (U_GOAL_q4_q2))
			(at end (U_GOAL_q2_q4))
		)
	)

	(:durative-action U_GOAL_action_4_2--q4--q3
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q3))
			(at start (NOT_U_GOAL_q4_q3))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q3)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q3))
			(at end (U_GOAL_q4_q3))
			(at end (U_GOAL_q3_q4))
		)
	)

	(:durative-action U_GOAL_action_4_2--q4--q4
		:parameters ()
		:duration (= ?duration 4)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q4))
			(at start (NOT_U_GOAL_q4_q4))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q4))
			(at end (U_GOAL_q4_q4))
			(at end (U_GOAL_q4_q4))
		)
	)

	(:durative-action U_GOAL_action_4_3--q1--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q1_q1))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (not (NOT_U_GOAL_q1_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q1_q1))
			(at end (U_GOAL_q1_q1))
		)
	)

	(:durative-action U_GOAL_action_4_3--q1--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q1_q2))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q1_q2))
			(at end (U_GOAL_q2_q1))
		)
	)

	(:durative-action U_GOAL_action_4_3--q1--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q1_q3))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q1_q3))
			(at end (U_GOAL_q3_q1))
		)
	)

	(:durative-action U_GOAL_action_4_3--q1--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q1_q4))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q1_q4))
			(at end (U_GOAL_q4_q1))
		)
	)

	(:durative-action U_GOAL_action_4_3--q2--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q2_q1))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q2_q1)))
			(at end (not (NOT_U_GOAL_q1_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q2_q1))
			(at end (U_GOAL_q1_q2))
		)
	)

	(:durative-action U_GOAL_action_4_3--q2--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q2_q2))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (not (NOT_U_GOAL_q2_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q2_q2))
			(at end (U_GOAL_q2_q2))
		)
	)

	(:durative-action U_GOAL_action_4_3--q2--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q2_q3))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q2_q3))
			(at end (U_GOAL_q3_q2))
		)
	)

	(:durative-action U_GOAL_action_4_3--q2--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q2_q4))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q2_q4))
			(at end (U_GOAL_q4_q2))
		)
	)

	(:durative-action U_GOAL_action_4_3--q3--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q3_q1))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q3_q1)))
			(at end (not (NOT_U_GOAL_q1_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q3_q1))
			(at end (U_GOAL_q1_q3))
		)
	)

	(:durative-action U_GOAL_action_4_3--q3--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q3_q2))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q3_q2)))
			(at end (not (NOT_U_GOAL_q2_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q3_q2))
			(at end (U_GOAL_q2_q3))
		)
	)

	(:durative-action U_GOAL_action_4_3--q3--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q3_q3))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (not (NOT_U_GOAL_q3_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q3_q3))
			(at end (U_GOAL_q3_q3))
		)
	)

	(:durative-action U_GOAL_action_4_3--q3--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q3_q4))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q3_q4))
			(at end (U_GOAL_q4_q3))
		)
	)

	(:durative-action U_GOAL_action_4_3--q4--q1
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q1))
			(at start (NOT_U_GOAL_q4_q1))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q1)))
			(at end (not (NOT_U_GOAL_q4_q1)))
			(at end (not (NOT_U_GOAL_q1_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q1))
			(at end (U_GOAL_q4_q1))
			(at end (U_GOAL_q1_q4))
		)
	)

	(:durative-action U_GOAL_action_4_3--q4--q2
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q2))
			(at start (NOT_U_GOAL_q4_q2))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q2)))
			(at end (not (NOT_U_GOAL_q4_q2)))
			(at end (not (NOT_U_GOAL_q2_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q2))
			(at end (U_GOAL_q4_q2))
			(at end (U_GOAL_q2_q4))
		)
	)

	(:durative-action U_GOAL_action_4_3--q4--q3
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q3))
			(at start (NOT_U_GOAL_q4_q3))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q3)))
			(at end (not (NOT_U_GOAL_q4_q3)))
			(at end (not (NOT_U_GOAL_q3_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q3))
			(at end (U_GOAL_q4_q3))
			(at end (U_GOAL_q3_q4))
		)
	)

	(:durative-action U_GOAL_action_4_3--q4--q4
		:parameters ()
		:duration (= ?duration 3)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q4))
			(at start (NOT_U_GOAL_q4_q4))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (not (NOT_U_GOAL_q4_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q4))
			(at end (U_GOAL_q4_q4))
			(at end (U_GOAL_q4_q4))
		)
	)

	(:durative-action swap_1_2--q1--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_1_2--q1--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_1_2--q1--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_1_2--q1--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_1_2--q2--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_1_2--q2--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_1_2--q2--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_1_2--q2--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_1_2--q3--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_1_2--q3--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_1_2--q3--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_1_2--q3--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_1_2--q4--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_1_2--q4--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_1_2--q4--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_1_2--q4--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_1_3--q1--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_1_3--q1--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_1_3--q1--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_1_3--q1--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q1))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_1_q1)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_1_3--q2--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_1_3--q2--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_1_3--q2--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_1_3--q2--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q2))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_1_q2)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_1_3--q3--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_1_3--q3--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_1_3--q3--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_1_3--q3--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q3))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_1_q3)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_1_3--q4--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_1_q1))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_1_3--q4--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_1_q2))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_1_3--q4--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_1_q3))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_1_3--q4--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_1_q4))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_1_q4)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_1_q4))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_4_2--q1--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_4_2--q1--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_4_2--q1--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_4_2--q1--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q1))
		)
	)

	(:durative-action swap_4_2--q2--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_4_2--q2--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_4_2--q2--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_4_2--q2--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q2))
		)
	)

	(:durative-action swap_4_2--q3--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_4_2--q3--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_4_2--q3--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_4_2--q3--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q3))
		)
	)

	(:durative-action swap_4_2--q4--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q1))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_4_2--q4--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q2))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_4_2--q4--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q3))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_4_2--q4--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_2_q4))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_2_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_2_q4))
		)
	)

	(:durative-action swap_4_3--q1--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_4_3--q1--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_4_3--q1--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_4_3--q1--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q1))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_4_q1)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q1))
		)
	)

	(:durative-action swap_4_3--q2--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_4_3--q2--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_4_3--q2--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_4_3--q2--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q2))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_4_q2)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q2))
		)
	)

	(:durative-action swap_4_3--q3--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_4_3--q3--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_4_3--q3--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_4_3--q3--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q3))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_4_q3)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q3))
		)
	)

	(:durative-action swap_4_3--q4--q1
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q1))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q1)))
			(at end (located_at_4_q1))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_4_3--q4--q2
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q2))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q2)))
			(at end (located_at_4_q2))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_4_3--q4--q3
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q3))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q3)))
			(at end (located_at_4_q3))
			(at end (located_at_3_q4))
		)
	)

	(:durative-action swap_4_3--q4--q4
		:parameters ()
		:duration (= ?duration 2)
		:condition (and
			(at start (located_at_4_q4))
			(at start (located_at_3_q4))
		)
		:effect (and
			(at start (not (located_at_4_q4)))
			(at start (not (located_at_3_q4)))
			(at end (located_at_4_q4))
			(at end (located_at_3_q4))
		)
	)

)
