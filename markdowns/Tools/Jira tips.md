
Jira can have **jql** statement, such as the following 

>project = "Jira Code" and "Epic Link" in (FITSOFF-256, FITSOFF-161) and status not in (Closed, Resolved)

you can input your own jql statement in and such as 

>"Epic Link" in (FITSOFF-256, FITSOF-161)

Not sure if you can support this style:

>"Epic Link" in ("FITSOFF-256", "FITSOF-161")


## Meet the New JIRA : Watch Issues in Bulk

while this note is based on the [Meet the New JIRA: Watch Issues in Bulk!](http://blogs.atlassian.com/2013/05/bulk-watch-meet-the-new-jira/). to summarize, it is as follow. 

1. Subscribe, you can do a filter by subscription, the following is what I get from the JQL .

```project = JIRA_CODE AND (assignee in ("6027849") OR Reviewer in ("6027849")) AND status NOT IN (Resolved, Closed)```

2. Save the Filter to some name, in my case, I have named it "Jira Code - Claud Duque Nicolas".

3. Subscribe to it 
Click "details", then you can try to subsscribe to that filter, 

Recipient: ...
Schedule: Daily 
Interval: 
   Subscribe 

3. Bulk watch, 

from the tools's dropdown box, there is a "all xxx Issues(s)", then  you can open the change wizard to show all the issues.  selects all the issues 

4. watch 

there are options, "Watch Issues" and "Stop Watching Issues" .



References:
[Meet the New JIRA: Watch Issues in Bulk!](http://blogs.atlassian.com/2013/05/bulk-watch-meet-the-new-jira/)