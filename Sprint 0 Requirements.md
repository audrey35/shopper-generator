# Sprint 0 & 1 Requirements
**Project Overview**

The project gives you an opportunity as a team to create a product based on (deliberately) vague and evolving requirements. There are 4 phases:

- **Phase 1:** Understand the problem, figure out where to start and get development environment up and running
- **Phase 2:** Build the initial core functionality you have planned.
- **Phase 3:** Extend the core functionality to make it useful
- **Phase 4:** Be creative and do wonderful, impressive things!!

You’ll be assessed after each phase by your Product Owner (TA/Professor)

Read on to get the initial details.

**Project Description**

This new situation with COVID-19 has thrown everything into chaos; in particular, grocery stores! Given the social distancing guidelines, grocery stores have to do something a little different to try to ensure there are enough workers on duty to keep customers moving through without bunching up and having to force people to wait outside. At the same time, the patterns of customers shopping have changed. The manager of my local Met Market was telling me how tough it is to apply their years of experience to these changes in circumstances for operational planning, and they know that whatever they do now is going to change soon again. They have recently installed some technology that tracks the number of customers and how they go through the store, but just got it installed right before everything changed, so they haven't had a chance to do anything with the data yet.

I was looking for a new project to do this summer, so I told the manager I could write some software that would generate data to allow them to do some operational planning. In particular, I could allow them to specify different parameters so that they could do planning for now AND later, when customers go back to more "normal" schedules.

He gave me the following data:

Our average shopper traffic numbers for each day are:

- Monday: .8k
- Tuesday: 1k
- Wednesday: 1.2K
- Thursday: .9K
- Friday: 2.5K
- Saturday: 4K
- Sunday: 5K

Holidays are about 20% of the normal traffic, but the day before a holiday is 40% higher than normal, and the week leading up to a holiday is about 15% higher than normal.

We open at 6am and close at 9pm. On Tuesdays 10am-12pm, we offer an extra senior discount, so we get more seniors in that time. Seniors tend to take about 45-60 minutes shopping.

At lunchtime during the week, we usually have people run in to grab prepared foods for lunch. Between 12-1pm, there are more customers, but the trips are very short (about 10 minutes).

At dinnertime during the week (from about 5-6:30pm), we once again have a rush; this is usually people running in to grab something for dinner. Trips are relatively short, about 20 minutes; but most of that is waiting in line. We expect that if we can get the right number of people working, that time will go down.

On weekends, we get more people doing their weekly grocery shopping. Trips are more like 60 minutes. But if the weather is really nice, we have more people (about 40% more!) stopping by to get grab and go food (so short visits).

Generally shoppers spend about 25 minutes in the store. The distribution ranges from about 6 minutes on the super-fast end, to about 75 minutes on the long end.

The Manager asked if I could generate a .csv file, with each row representing a shopper during a day and how long they spend in the store. Then, they can play around with it and try out some planning exercises.

# Sprint 0: Planning for Sprint 1

**[Edited: Added "Addressing Questions" section, below]**

This is your first step in the project!

The primary goal here is to get set up to run your first sprint. That means you have a lot of planning to do and decisions to make!

Try and figure out what the above info means. **Ask lots of questions of your Instructors.**

**Scope your first sprint.** Capture this scope as User Stories in Trello with appropriate story points and task breakdowns. By including user stories in your sprint, you are committing to deliver these by the end of the sprint.

**Specify your tool chain and development environment.** We assume Java as your main programming language, although you are free to choose any you like.

**Use a CCIS git repo for team code and development management.** You will also submit additional assessment documents through this repo in subsequent phases.

Create a document that:

1. Contains the URL for your Trello board
2. Lists your user stories
3. Sketches out the initial design of what you propose to build. One way is to specify your inputs, the major abstractions in your solution for the first set of user stories, and your outputs.

The whole document should be no more than 4 pages.

Put this document in your git repo, in a folder called Sprint 0. Also submit the .pdf file on Canvas.

See rubric for grading criteria.

**Updates: Addressing Questions**

- You don't HAVE to use Trello, but it's an easy way to get started.
    - Trello has a [blog post](https://blog.trello.com/how-to-scrum-and-trello-for-teams-at-work) detailing a good way to use Trello with a Scrum process.
    - I thought this [blog post](https://blog.hubstaff.com/agile-trello/) was also helpful.
- User Stories are not Use Cases
    - [This article](http://www.stellman-greene.com/2009/05/03/requirements-101-user-stories-vs-use-cases/) does a good job distinguishing the two.
- Every team is going to have a specified "Customer":
    - Project Groups 1-4: Adrienne is your customer
    - Project Groups 5-8: Alan
    - Project Groups 9-13: Minghao
    - Reach out to those customers for questions about requirements. We might provide slightly different answers, as 3 different customers, and that's okay. Listen to YOUR team's customer :)
- I **DO** want you to use a Scrum process for your project. [Here's an infographic](https://www.nutcache.com/blog/agile-scrum-development-process-demystified-in-5-minutes/) that lays out the process fairly concretely but without too much overwhelming detail.

**Criteria**

- Trello Board: User stories defined, Trello board organized for SCRUM, story points assigned
- Design
    - Inputs specified
    - Outputs specified
    - Major abstractions and relationships identified
    - Programming language and external libraries identified