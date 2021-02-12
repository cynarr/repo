from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse


BAD_PARAM_PREFIXES = [
    "ga_",
    "utm_",
    "pk_",
    "sc_",
    "itm_",
    "fb_",
]

BAD_PARAMS = [
    "mkt_tok",
    "action_object_map",
    "action_type_map",
    "action_ref_map",
    "aff_platform",
    "aff_trace_key",
    "mkt_tok",
    "trk",
    "trkCampaign",
    "hmb_campaign",
    "hmb_medium",
    "hmb_source",
    "yclid",
    "_openstat",
    "mbid",
    "cmpid",
    "cid",
    "c_id",
    "campaign_id",
    "Campaign",
    "fbclid",
    "gs_l",
    "_hsenc",
    "_hsmi",
    "__hssc",
    "__hstc",
    "hsCtaTracking",
    "spReportId",
    "spJobID",
    "spUserID",
    "spMailingID",
    "elqTrackId",
    "elqTrack",
    "assetType",
    "assetId",
    "recipientId",
    "campaignId",
    "siteId",
    "wt_zmc",
    "tid",
    "aip",
    "ds",
    "qt",
    "cid",
    "uid",
    "uip",
    "ua",
    "geoid",
    "dr",
    "cn",
    "cs",
    "cm",
    "ck",
    "cc",
    "ci",
    "gclid",
    "dclid",
    "linkid",
    "icid",
    "sr_share",
    "iid",
    "ijn",
    "ncid",
    "nid",
    "ref",
    "smid",
]


def remove_params():
    params = []
    for param, values in parse_qs(query_string).items():
        if (
            not any((
                param.startswith(bad_prefix)
                for bad_prefix
                in BAD_PARAM_PREFIXES
            ))
            and param not in params_to_remove
        ):
            for value in values:
                params.append((param, value))
    return urlencode(params)


def urlnorm(url):
    from w3lib.url import canonicalize_url
    parsed = urlparse(url)
    parsed = parsed._replace(query=remove_params(parsed.query))
    parsed.geturl()
    canonicalize_url(url, keep_blank_values=False)
