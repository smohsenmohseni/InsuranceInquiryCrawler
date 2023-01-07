ATIEH_INSURANCE_INFO = {
    'login_url': 'https://rasatpa.ir/sso/login?service=https%3A%2F%2Frasatpa.ir%2Fhcp%2Flogin%2Fcas',
    'inquiry_url': 'https://rasatpa.ir/hcp/reception/inquiryInsuredPerson',
    'login_data': {
        'username': '44443148',
        'password': 'moein999',
        'execution': 'e1s1',
        '_eventId': 'submit',
    },
}

DANA_INSURANCE_INFO = {
    'login_url': 'https://totalapp2.dana-insurance.ir/Sepad1/Security',
    'inquiry_url': (
        'https://totalapp2.dana-insurance.ir/Sepad1/Fanavaran/'
        'GetDataBimenameBimeShodeFanByCodeMeliTarikh?tarikhHazine=1401/10/13&CodeMelli={national_code}'
    ),
    'login_data': {
        'NameKarbari': 'mp1201451',
        'RamzeObor': 'moein999',
    },
}

IRAN_INSURANCE_INFO = {
    'login_url': (
        'https://darman.iraninsurance.ir/dms-cas/'
        'login?service=http%3A%2F%2Fdarman.iraninsurance.ir%2F%2Fj_spring_cas_security_check'
    ),
    'inquiry_url': 'http://darman.iraninsurance.ir/home-flow?execution=e1s1',
    'login_data': {
        'username': '444431488',
        'password': 'moein999',
    },
}

MAD_ASIA_INSURANCE_INFO = {
    'login_url': 'https://mccp.iraneit.com/core/connect/token',
    'inquiry_url': (
        "https://mccp.iraneit.com/odata/MCClaimProc/preAuthEnabledPolicy/"
        "getInsuredPersonPolicyInfo(corpId=155,nationalCodeOrId='{national_code}',type='nationalcode')?$top=1"
    ),
    'login_data': {
        'scope': 'openid profile user_info',
        'grant_type': 'password',
        'username': 'l.tehran11001',
        'password': 'abc123',
        'client_id': 'MCClaimProc-ResOwner',
        'client_secret': 'secret',
    },
}

SOS_INSURANCE_INFO = {
    'login_url': 'https://carewrapper.iranassistance.com/Auth/Authentication/LoginUser',
    'inquiry_url': 'https://carewrapper.iranassistance.com/api/CareCenter/GetContractList',
}

TAMIN_INSURANCE_INFO = {
    'inquiry_url': 'https://medical.tamin.ir/api/medical-support/v2.0/{national_code}',
}
