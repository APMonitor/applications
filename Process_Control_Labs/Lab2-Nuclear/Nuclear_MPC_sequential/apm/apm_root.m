% Open APM Root Folder
function [stat] = apm_root(server,app)
   % get ip address for web-address lookup
   ip = deblank(urlread([deblank(server) '/ip.php']));
   app = deblank(app);
   url = [deblank(server) '/online/' ip '_' app '/'];

   % load web-interface in default browser
   stat = web(url,'-browser');  % doesn't work in some older MATLAB versions
