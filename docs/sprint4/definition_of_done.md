# Definition of done sprint 4
To get an overview of tasks for sprint 4, you can type in milestone = sprint 4 and hit enter on gitlab boards.
Note: All task breakdowns for mentioned issues can be found within the issue itself on gitlab.

### Definite web socket integrations:
These are the user stories we will introduce to the web socket interface this sprint:
- [x] [Issue #100] Get all candidates in election
- [x] [Issue #97] As a user I want to be able to see the results of all polls of the same election
- [x] [Issue #99] As a user I would like to get a single election by ID
- [x] [Issue #98] As a user I would like to get all elections
- [x] [Issue #22] As a user I would like to create a poll, so that other people can vote on it
- [x] [Issue #96] As a user I want to have the option to filter for polls in a specific time frame
- [x] [Issue #95] As a user I want to have the option to filter between different poll source

### Websocket integrations
These user stories would create web socket connections with the following format (subject to minor naming changes)
- [X] getCandidates(electionID)
- [x] getOverallElectionPoll(electionID)
- [x] getElection(electionID)
- [x] getElections()
- [x] createPoll()
- [x] getHistoricalPollsForElection(electionID, dateAfter, dateBefore)
- [x] getPollsBySourceName(election ID, organizationID)

### Additional issues that we will introduce:
These are additional issues that we will introduce alongside the web socket integrations:
- [x] [Issue #104] Introduce electable and party to project\
This issue will be further introduced in later sprints, once the idea is definite in the frontend. However has been integrated in auth methods.
- [x] [Issue #102] Increase time efficiency of poll calculations
- [x] [Issue #101] Increase time efficiency of vote calculations


## Additional integrations if time allows:
Sub tasks within issue #22 that are not directly connected to the method itself\
Updating candidate model to return electable (Sub task in issue #104)

#### Additionally Integrated:
- [x] createUser
- [x] login
- [x] logout
- [x] vote
- [x] createPoll
- [x] createElectable
- [x] getUserElectables
- [x] deleteElectable
- [x] createElection
- [x] deleteElection
- [x] addElectionRegion
- [x] addElectionElectable
- [x] getUserElections
- [x] deletePoll
- [x] getUserPolls

The security was evaluated in the authentication package. **The component is completely separate** from other parts of the project and only **integrated using the auth API** via the interface layer and can be **decoupled by simply removing the auth import** from communicator.py. The users **sensitive information is kept unreachable** after creation of users. The same goes for the actual password and username of a user after he logs in.

The vote choice of users is not stored in the users creation information to **ensure user privacy** if some information got leaked. The password is encoded using **sha256 (usn+pw)**. All relations between users and created objects in original project are stored in the authentication model under user_creations. _No backend models were modified in the original project to implement the relations_. 