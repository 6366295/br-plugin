package vu.thesis.mike.broadcastreceiverplugin;

import com.intellij.openapi.actionSystem.*;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class HelloAction extends AnAction {
    public HelloAction() {
        super("Hello");
    }

    public void actionPerformed(AnActionEvent event) {
        Project project = event.getProject();

        try {
            String[] args = new String[] {"/bin/sh", "-c", "gnome-terminal -x python /home/mt/Thesis/ToolChain/BroadcastReceiverExerciser"};
            Process proc = new ProcessBuilder(args).start();

//            proc.waitFor();
//            BufferedReader buf = new BufferedReader(new InputStreamReader(proc.getInputStream()));
//            String line = "";
//            while ((line=buf.readLine())!=null) {
//                Messages.showMessageDialog(project, line, "Greeting", Messages.getInformationIcon());
//            }
        } catch (Exception e) {

        }


    }
}