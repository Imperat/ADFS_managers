#include <stdbool.h>

unsigned int getpoints(int first_goals, int second_goals, bool isHome) {
  if (first_goals == second_goals) {
    return 1;
  }

  if (!isHome) {
    int tmp = first_goals;
    first_goals = second_goals;
    second_goals = tmp;
  }

  if (first_goals > second_goals) {
    return 3;
  }

  return 0;
}
