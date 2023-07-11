import sys

from pprint import pprint

from splunklib.client import Service, Job, SavedSearch, AlertGroup, connect, Entity
from splunklib.results import JSONResultsReader


def pretty(source_stream=sys.stdin, name="results"):
    pprint(name)
    reader = JSONResultsReader(source_stream)
    for event in reader:
        pprint(event)


def service_connect(
    host="10.8.4.12",
    port="8089",
    username="user_name",
    password="******",
):
    service: Service = connect(
        host=host,
        port=port,
        username=username,
        password=password,
        autologin=True,
        # verify=False,
        # scheme="http",
    )
    print("Connected: ", service.info["master_uri"])

    return service


def saved_searches(service: Service):
    jobs = service.jobs
    # print(jobs.get(""))
    # jobs.iter(pagesize=30)
    # GET
    jobs_dict: dict[str, Job] = {
        job.sid: job
        for job in
        jobs.list()
    }

    # exported_jobs = jobs.export("search * | head 10", output_mode='json')
    # print(type(exported_jobs))
    # pretty(exported_jobs, name="Jobs exported")
    # GET
    alert_groups_list = service.fired_alerts.list()
    print("Alert groups count: ", len(alert_groups_list))
    alert_groups_list.sort(key=lambda x: x.name)
    alert_group_names = (alert_group.name for alert_group in alert_groups_list)
    print("alert_group_names:", tuple(alert_group_names))

    for alert_group in alert_groups_list:
        alert_group: AlertGroup
        if alert_group.name == "-":  # this group is for all alerts
            continue
        # "we could choose certain alert name"
        alert_list = alert_group.alerts.list()
        print("fired_alerts for alert_group:", alert_group.name)
        print("job(scheduler) count:", len(alert_list))
        # GET
        for job_scheduler in alert_list:
            job_scheduler: Entity
            print(f"===={job_scheduler.name}")
            # print(job_scheduler.links)

            # "content":
            # "actions"(['telegram'])
            # "savedsearch_name" "sid"
            # "severity"("3")
            # 'trigger_time_rendered' 'triggered_alerts'(count)

            # job: Job = service.jobs(job_scheduler.content["sid"])
            job: Job = jobs_dict.get(job_scheduler.content["sid"])
            # print(job.content)
            if job:
                pretty(
                    # GET
                    job.results(
                        output_mode="json", is_preview=True, add_summary_to_metadata=True
                    ),
                    name="job results",
                )

        # break

    # for saved_search in service.saved_searches:
    #     saved_search: SavedSearch
    #     if saved_search.name not in ("Alert name here", ):
    #         continue
    #     print(saved_search.name)
    #     print('=' * len(saved_search.name))
    #     # content = saved_search.content
    #     # fields = saved_search.fields
    #     # print("fields:", fields)
    #
    #     # try-catch:
    #     # fired_alerts = saved_search.fired_alerts
    #     # print("fired_alerts:")
    #     # for fired_alert in fired_alerts:
    #     #     fired_alert: AlertGroup
    #     #     for job_scheduler in fired_alert.alerts:
    #     #         print(type(job_scheduler))
    #     #         print(job_scheduler.__dict__)
    #
    #     history = saved_search.history()
    #     # if len(history) > 0:
    #     #     print("history:")
    #
    #     for job in history:
    #         job: Job
    #         print(f"-----{job.sid}")  #," {job.name}")
    #         # job result is reachable just for finished jobs
    #         pretty(job.results(output_mode="json", is_preview=True), name="job results")
    #         print()
    #
    #         # pretty(job.events(output_mode="json", is_preview=True), name="job events")
    #
    #         # print(job.links, "\n")
    #
    #         # print(job.state, "\n")
    #         # print(job.access, "\n")
    #
    #         # "label"(saved_search name) "eventCount"
    #         # time period: "earliestTime" "latestTime"
    #         # "eventSearch" "optimizedSearch"
    #         # "searchProviders"(indexes)
    #         # print(job.content, "\n")
    #         # print(job.defaults, "\n")
    #
    #         pretty(job.summary(output_mode="json", is_preview=True), name="summary")
    #         # pretty(job.searchlog(output_mode="json", is_preview=True), name="searchlog")
    #         pretty(job.timeline(output_mode="json", is_preview=True), name="timeline")
    #         print()
    #     else:
    #         continue
    #     # for key in sorted(content.keys()):
    #     #     value = content[key]
    #     #     print(f"{key}: {value}")
    #     print()
    #     break


if __name__ == "__main__":
    service = service_connect()

    saved_searches(service)

    service.logout()
