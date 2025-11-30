"""
Scoring strategies for different question types.

Implements the Strategy Pattern for better extensibility and adherence to the
Open/Closed Principle (OCP).
"""

from abc import ABC, abstractmethod
from typing import List, Set
from .models import Question


class QuestionScoringStrategy(ABC):
    """
    Abstract base class for question scoring strategies.

    Defines the interface that all concrete strategies must implement.
    """

    @abstractmethod
    def is_correct(self, question: Question, submitted_answer_ids: List[int]) -> bool:
        """
        Determine if the submitted answers are correct for the given question.

        Args:
            question: The Question instance being evaluated
            submitted_answer_ids: List of answer IDs submitted by the user

        Returns:
            True if the answer is correct, False otherwise
        """
        pass


class SingleChoiceStrategy(QuestionScoringStrategy):
    """
    Scoring strategy for single-choice questions.

    A single-choice question is correct if:
    - Exactly one answer is submitted
    - That answer is the correct one
    """

    def is_correct(self, question: Question, submitted_answer_ids: List[int]) -> bool:
        correct_answer_ids: Set[int] = set(
            question.answers.filter(is_correct=True).values_list('id', flat=True)
        )
        submitted_ids: Set[int] = set(submitted_answer_ids)

        # Must have exactly one submission that matches the one correct answer
        return (
            len(submitted_ids) == 1 and
            len(correct_answer_ids) == 1 and
            submitted_ids == correct_answer_ids
        )


class MultipleChoiceStrategy(QuestionScoringStrategy):
    """
    Scoring strategy for multiple-choice questions.

    A multiple-choice question is correct if:
    - All correct answers are selected
    - No incorrect answers are selected
    """

    def is_correct(self, question: Question, submitted_answer_ids: List[int]) -> bool:
        correct_answer_ids: Set[int] = set(
            question.answers.filter(is_correct=True).values_list('id', flat=True)
        )
        submitted_ids: Set[int] = set(submitted_answer_ids)

        # Submitted answers must exactly match correct answers
        return submitted_ids == correct_answer_ids


class SelectWordsStrategy(QuestionScoringStrategy):
    """
    Scoring strategy for select-words questions.

    Similar to multiple-choice: all correct words must be selected,
    and no incorrect words should be selected.
    """

    def is_correct(self, question: Question, submitted_answer_ids: List[int]) -> bool:
        correct_answer_ids: Set[int] = set(
            question.answers.filter(is_correct=True).values_list('id', flat=True)
        )
        submitted_ids: Set[int] = set(submitted_answer_ids)

        # Submitted answers must exactly match correct answers
        return submitted_ids == correct_answer_ids


class ScoringStrategyFactory:
    """
    Factory for creating appropriate scoring strategies based on question type.

    This implements the Factory Pattern to decouple strategy instantiation
    from the scoring service.
    """

    # Registry mapping question types to their strategies
    _strategies = {
        'single': SingleChoiceStrategy,
        'multi': MultipleChoiceStrategy,
        'select_words': SelectWordsStrategy,
    }

    @classmethod
    def get_strategy(cls, question_type: str) -> QuestionScoringStrategy:
        """
        Get the appropriate scoring strategy for a question type.

        Args:
            question_type: The type of question (e.g., 'single', 'multi')

        Returns:
            An instance of the appropriate scoring strategy

        Raises:
            ValueError: If the question type is not recognized
        """
        strategy_class = cls._strategies.get(question_type)
        if not strategy_class:
            raise ValueError(
                f"Unknown question type '{question_type}'. "
                f"Supported types: {', '.join(cls._strategies.keys())}"
            )
        return strategy_class()

    @classmethod
    def register_strategy(cls, question_type: str, strategy_class: type) -> None:
        """
        Register a new scoring strategy for a question type.

        This allows for easy extension with new question types without
        modifying existing code (Open/Closed Principle).

        Args:
            question_type: The question type identifier
            strategy_class: The strategy class to use for this question type

        Example:
            >>> class TrueFalseStrategy(QuestionScoringStrategy):
            ...     def is_correct(self, question, submitted):
            ...         # Implementation
            ...         pass
            >>> ScoringStrategyFactory.register_strategy('true_false', TrueFalseStrategy)
        """
        if not issubclass(strategy_class, QuestionScoringStrategy):
            raise TypeError(
                f"{strategy_class.__name__} must inherit from QuestionScoringStrategy"
            )
        cls._strategies[question_type] = strategy_class
