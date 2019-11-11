CREATE TABLE `LocalMRIQuestionnaire` (
`CommentID` varchar(255) NOT NULL default '',
                          `UserID` varchar(255) default NULL,
                          `Examiner` varchar(255) default NULL,
                          `Testdate` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                          `Data_entry_completion_status` enum('Incomplete','Complete') NOT NULL default 'Incomplete',
`Date_taken` date default NULL,
`Candidate_Age` varchar(255) default NULL,
`Window_Difference` varchar(255) default NULL,
`MRN` numeric default NULL,
`MRN_status` enum('not_answered') default NULL,
`CNBPID` varchar(255) default NULL,
`CNBPID_status` enum('not_answered') default NULL,
`BirthWeight` numeric default NULL,
`BirthWeight_status` enum('not_answered') default NULL,
`birthdate_date` date default NULL,
`birthdate_date_status` enum('not_answered') default NULL,
`BirthTime` varchar(255) default NULL,
`BirthTime_status` enum('not_answered') default NULL,
`mridate_date` date default NULL,
`mridate_date_status` enum('not_answered') default NULL,
`MRIReason` varchar(255) default NULL,
`MRIDx` varchar(255) default NULL,
`LocalEntryTimeStamp` varchar(255) default NULL,
`LocalEntryTimeStamp_status` enum('not_answered') default NULL,
`LocalUserID` numeric default NULL,
`LocalUserID_status` enum('not_answered') default NULL,
`MRIAge` numeric default NULL,
`MRIAge_status` enum('not_answered') default NULL,
PRIMARY KEY  (`CommentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
REPLACE INTO test_names (Test_name, Full_name, Sub_group) VALUES ('LocalMRIQuestionnaire', 'LocalMRIQuestionnaire', 1);