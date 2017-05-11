{
  "name": "mjf_inout",
  "userId": "learning",
  "rules": [
    {
      "conditions": [
        {
          "condition": "inout.deviceType == client"
        },
        {
          "condition": "inout.hierarchy == DevNetCampus>DevNetBuilding>DevNetZone>Zone2"
        }
      ]
    }
  ],
  "subscribers": [
    {
      "receivers": [
        {
          "uri": "http://128.107.70.29:8000",
          "messageFormat": "JSON",
          "qos": "AT_MOST_ONCE"
        }
      ]
    }
  ],
  "enabled": true,
  "enableMacScrambling": true,
  "macScramblingSalt": "inout",
  "notificationType": "InOut"
}
