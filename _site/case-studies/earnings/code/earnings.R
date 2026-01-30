# open data morg in not shared folder

library(tidyverse)

path="not-shared/"
morg <- read_csv(paste0(path, "morg-2014-emp.csv"))

# ordered freq table of state
morg %>%
  group_by(state) %>%
  summarise(n = n()) %>%
  arrange(desc(n)) %>%
  mutate(state = fct_reorder(state, n)) %>%
  ggplot(aes(x = state, y = n)) +
  geom_col() +
  coord_flip() +
  labs(title = "Number of Employees by State in Morg",
       x = "State",
       y = "Number of Employees") +
  theme_minimal()

# find the largest state in terms of number of obs

morg2=morg %>%
  group_by(state) %>%
  summarise(n = n()) %>%
  arrange(desc(n)) %>%
  slice(1) %>%
  pull(state)


# filter morg for the largest state
morg_largest_state <- morg %>%
  filter(state == morg2)


# describe age
morg_largest_state %>%
  summarise(mean_age = mean(age, na.rm = TRUE),
            median_age = median(age, na.rm = TRUE),
            sd_age = sd(age, na.rm = TRUE),
            min_age = min(age, na.rm = TRUE),
            max_age = max(age, na.rm = TRUE))

# show histogram of age, bandwidth of 1
morg_largest_state %>%
  ggplot(aes(x = age)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black", alpha = 0.7) +
  labs(title = "Age Distribution in Largest State",
       x = "Age",
       y = "Frequency") +
  theme_minimal()
