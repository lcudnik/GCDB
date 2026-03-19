Import-Module "$PSScriptRoot\components\skyapi\ps_skyapi\SKYAPI.psm1"

$outputLocation = "\\ub-g-script\c$\Scripts\local_assets\bb"

Set-SKYAPIConfigFilePath -Path "$outputLocation\ps_skyapi\Config\sky_api_config.json" # The location where you placed your Blackbaud SKY API configuration file.
Set-SKYAPITokensFilePath -Path "$outputLocation\ps_skyapi\Config\skyapi_key.json" # The location where you want the access and refresh tokens to be stored.

$apiKeys = Get-Content -Path "$outputLocation\skyapi.json" | ConvertFrom-Json -AsHashtable

try {
    Connect-SKYAPI -ForceRefresh
}
catch {
    Connect-SKYAPI -ForceReauthentication
}

$AuthTokensFromFile = Get-SKYAPIAuthTokensFromFile

$apiKeys.refresh_token = $AuthTokensFromFile.refresh_token
$apiKeys.accessToken =  $AuthTokensFromFile.access_token

$apiKeys | ConvertTo-Json | Out-File -FilePath "$outputLocation\skyapi.json"

