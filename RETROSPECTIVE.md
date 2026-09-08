# I built an AI recruiter for my job search. The scanning was the least useful part.

Five months ago I started looking for my next role. I've led sales engineering teams for a long time, and I've watched job searching turn into something that happens agent to agent. Companies run AI over the applications. Candidates use AI to write them. The first reader of most applications isn't a person anymore.

So I built my own agent for the search. It ran on Claude Code, wrote everything to a folder of notes on my laptop, and never sent a message on my behalf. Last week I accepted a leadership role at an AI company here in Austin. I start in a few days.

This is what the agent did, what it didn't do, and what I'd tell anyone who is mid-search right now. The tools are public, and they're at the end.

## The machine work

The agent did a lot of work. It created folders on 258 companies. It wrote 498 notes on individual roles and scored 457 of them against a rubric I gave it. It read my inbox every morning and triaged recruiter email, 190 messages in the last month of digests alone. It ran 89 scheduled overnight routines and checked careers pages 154 times looking for one specific kind of job. In total it produced about 803,000 words of research, briefs, prep notes, and market analysis. That's more than the first five Harry Potter books, except every page is about getting me hired.

I wrote almost none of that. And here's the part that surprised me. The scanning, the thing I assumed would be the whole point, found none of the roles that converted. Not one.

## Where my hours went

While the agent moved the bits and bytes, I spent my time on people.

That wasn't a nice sentiment. It was the agent's most useful job. It read my network against my target list and kept surfacing specific people, one or two degrees away, at companies I cared about. It tied each person to an application I had open. It told me which ones to hold in reserve so I never approached two people at the same company in the same week. One pass through my old colleagues found people I already knew at three of my top targets, each one sitting near a live application I had written off as cold.

Dozens of people surfaced that way. Dozens of conversations came out of it. For the roles that mattered, the agent named the recruiter, the hiring manager, the manager's boss, and a peer on the team, across 38 companies. It logged 76 interactions and 18 live calls and interviews. Every one of those conversations was mine to have. The agent made sure I knew who to have them with.

The design choice behind all of this: I gave the agent a recruiter's job, not a job board's. Scanning was one function among 25. The rest was the work a good recruiter does for one candidate. Know the market. Know the person. Know who to call. Get them ready.

## A numbers game and a judgment game

A job search compounds. Contacts lead to listings you hear about early. Some of those become applications with a person attached. Some of those become interviews. One person feeding that chain alone runs out of hours by week three and out of morale by week eleven. That's where solo searches die.

The agent doesn't get tired. It kept every stage of that chain fed for nineteen weeks. It never had a discouraged Tuesday.

The numbers it kept high were coverage and preparation. Not applications. I sent 29 in five months. Outreach was capped at three new people a day and ten a week, on purpose, because the fastest way to get flagged as an AI spammer is to act like one. High signal, never high volume.

I kept the judgment. Which roles I actually wanted. Which lane to pursue when the market told me to change lanes. Which people to reach and what to say to them. Every send.

## Lesson one: the job I wanted had a different name

Over five months the agent logged 405 distinct job titles for the one function I was targeting. Four hundred and five names for roughly the same job.

Its market analysis kept coming back to the same finding. The role I'd done for fifteen years was being posted under a new title at AI companies. Same work, different name. Most of my notes carried the old title. The ones that mattered carried the new one.

So I changed my profile preferences and my saved search terms to match. Three weeks later the listing I ended up accepting showed up in my feed under the new name. The crawler never found it. The rename did.

If you take one thing from this post: read ten postings at companies you'd love to join, note what they call your role, and feed those exact terms into your profile and your saved searches. The matching layer can only find you if you speak its current language. *(In the repo this is `/title-audit`. It reads the postings and hands you the terms.)*

## Lesson two: attach a human before you apply

After every rejection the agent wrote a postmortem and logged what the objection probably was. Nine rejections, nine postmortems, one pattern: every single loss was a cold application with no human attached. Not most. All.

The funnel said the same thing. Cold applications converted to a screen 12 percent of the time. Once I got to a screen, I converted to a hiring-manager round 67 percent of the time. The story worked whenever a person heard it. It lost in the pile.

The one that converted had a former colleague inside and a recruiter who championed it. I was aiming for 70 percent of applications to have a human attached. I peaked around a third. That gap is the whole search in one number.

Find someone at the company first, even two degrees out. Let the application follow the conversation by a couple of days, so a mention inside the building lands before your resume hits the pile. *(In the repo: `/warm-path`. It walks the ladder of who you know and reports your ratio.)*

## Lesson three: spend AI on depth, not volume

Everyone can mass-apply now. That's exactly why it stopped working.

The process I won ran five interview rounds in twenty days. I walked into every one with a research brief for that round, a profile on every person across the table (six of them at the on-site), a one-page card of what the round was really about, and my own stories rehearsed in mock interviews. The agent wrote about 27,500 words of preparation for that one company. By the end I knew their case studies better than my own resume.

Across the search it produced 33 deep company evaluations, 34 cover letters that started from research instead of a blank page, and a library of six career stories it rotated so no interviewer heard the same one twice.

That's where the time an agent saves you should go. Not into more applications. Into the rooms. *(In the repo: `/jobs-prep`, `/mock-interview`, `/day-of-card`, `/story`.)*

## Lesson four: keep your hands on everything that leaves

Recruiters read AI-written messages all day and they can tell. One detected template quietly ends a conversation, and the people in your field talk to each other.

So every draft the agent wrote came with a list of claims to verify and a source to read before I sent it, plus slots I had to fill in my own words. Each message had to carry one fact that took real work to find and one thing only I could say. Missing either, it didn't go. The agent drafted 52 outreach messages and queued 39 follow-ups. I sent every one of them by hand, at human hours, in my words. *(In the repo: `/voice-check`. It flags the tells before you hit send.)*

## What it never did

It never sent a message. It never mass-applied. It sat in zero interviews. It didn't replace the recruiter who championed me or the former colleague who put in a word. Its scanner indexed 258 companies and found none of the roles that converted.

## The hours, and an honest estimate

Priced at human rates, reproducing what the agent wrote comes to roughly a thousand hours. The math isn't exotic. The daily scan, inbox triage, and morning briefing is about five hours of analyst work, and it ran for 96 business days. The deep company evaluations take most of a day each. Cover letters run about ninety minutes apiece. Add interview prep, outreach drafts, and the postmortems and it lands between 800 and 1,300 hours. Call it six months of a full-time professional in my corner, running while I did my day job. That's an estimate from word counts, not a time sheet.

Here's the uncomfortable version. A good human recruiter would have spent about a hundred hours on me, and would probably have landed the same offer. The role came from a listing I clicked, warmed by a colleague, won in five rooms.

What the extra nine hundred hours bought was the work no human could afford to do for one candidate. It caught the winning thread in my inbox the week it went live. It prepared me for every round and every interviewer. It studied nine losses hard enough to find the pattern that changed the back half of my search. Maybe 150 of those hours were genuinely different. The rest were nearly free to produce, and mostly didn't convert.

For what it's worth, the first version of this ran on API calls and cost about $25 in total. After that it ran on a subscription. The marginal cost of another brief, another profile, another postmortem was zero.

## The cost of output went to zero. The cost of judgment didn't.

Hiring already runs agent to agent. Companies screen with AI, candidates apply with AI, and both sides are getting better at it. I think that's fine. Matching improves when the signal on both sides is true, and it collapses when either side starts templating.

The scarce things stayed scarce. A person in your corner. An honest read on why you lost. Being ready in the room. None of that got cheaper.

## The tools

I've cleaned up the agent and published it: [JobFinderOS](https://github.com/matthewprice/JobFinderOS). Three agents (a coach, a scout, and a market analyst), 25 skills, no API keys, and a fifteen-minute onboarding interview that works for any career. It runs on Claude Code and writes to a folder of notes you own.

It will find roles on employers' own careers pages, keep your pipeline honest, point you at people, prep you for every round, and tell you the truth at the end of every run. It will not send a message, mass-apply, or sit in an interview for you.

There are excellent open-source tools for applying well. This is the other half.

More soon on where I landed, and why I think the rename that found me this job is coming for a lot of our jobs next.
