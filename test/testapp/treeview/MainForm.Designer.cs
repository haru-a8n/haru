/*
 * Created by SharpDevelop.
 * User: Yng
 * Date: 7/18/2010
 * Time: 12:15 AM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
namespace treeview
{
	partial class MainForm
	{
		/// <summary>
		/// Designer variable used to keep track of non-visual components.
		/// </summary>
		private System.ComponentModel.IContainer components = null;
		
		/// <summary>
		/// Disposes resources used by the form.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing) {
				if (components != null) {
					components.Dispose();
				}
			}
			base.Dispose(disposing);
		}
		
		/// <summary>
		/// This method is required for Windows Forms designer support.
		/// Do not change the method contents inside the source code editor. The Forms designer might
		/// not be able to load this method if it was changed manually.
		/// </summary>
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			System.Windows.Forms.TreeNode treeNode1 = new System.Windows.Forms.TreeNode("AAA");
			System.Windows.Forms.TreeNode treeNode2 = new System.Windows.Forms.TreeNode("AA", new System.Windows.Forms.TreeNode[] {
									treeNode1});
			System.Windows.Forms.TreeNode treeNode3 = new System.Windows.Forms.TreeNode("A", new System.Windows.Forms.TreeNode[] {
									treeNode2});
			System.Windows.Forms.TreeNode treeNode4 = new System.Windows.Forms.TreeNode("Root", new System.Windows.Forms.TreeNode[] {
									treeNode3});
			System.Windows.Forms.TreeNode treeNode5 = new System.Windows.Forms.TreeNode("Root2");
			this.tvTest = new System.Windows.Forms.TreeView();
			this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
			this.aToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.bToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.cToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.dToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.aAToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.aBToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.aCToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.aAAToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
			this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
			this.contextMenuStrip1.SuspendLayout();
			this.SuspendLayout();
			// 
			// tvTest
			// 
			this.tvTest.ContextMenuStrip = this.contextMenuStrip1;
			this.tvTest.Dock = System.Windows.Forms.DockStyle.Fill;
			this.tvTest.Location = new System.Drawing.Point(0, 0);
			this.tvTest.Name = "tvTest";
			treeNode1.Name = "Node4";
			treeNode1.Text = "AAA";
			treeNode2.Name = "Node3";
			treeNode2.Text = "AA";
			treeNode3.Name = "Node2";
			treeNode3.Text = "A";
			treeNode4.Name = "Node0";
			treeNode4.Text = "Root";
			treeNode5.Name = "Node1";
			treeNode5.Text = "Root2";
			this.tvTest.Nodes.AddRange(new System.Windows.Forms.TreeNode[] {
									treeNode4,
									treeNode5});
			this.tvTest.Size = new System.Drawing.Size(292, 273);
			this.tvTest.TabIndex = 0;
			// 
			// contextMenuStrip1
			// 
			this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
									this.aToolStripMenuItem,
									this.toolStripSeparator1,
									this.bToolStripMenuItem,
									this.cToolStripMenuItem,
									this.dToolStripMenuItem});
			this.contextMenuStrip1.Name = "contextMenuStrip1";
			this.contextMenuStrip1.RenderMode = System.Windows.Forms.ToolStripRenderMode.System;
			this.contextMenuStrip1.Size = new System.Drawing.Size(153, 120);
			// 
			// aToolStripMenuItem
			// 
			this.aToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
									this.aAToolStripMenuItem,
									this.aBToolStripMenuItem,
									this.aCToolStripMenuItem});
			this.aToolStripMenuItem.Name = "aToolStripMenuItem";
			this.aToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.aToolStripMenuItem.Text = "A";
			// 
			// bToolStripMenuItem
			// 
			this.bToolStripMenuItem.Name = "bToolStripMenuItem";
			this.bToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.bToolStripMenuItem.Text = "B";
			// 
			// cToolStripMenuItem
			// 
			this.cToolStripMenuItem.Name = "cToolStripMenuItem";
			this.cToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.cToolStripMenuItem.Text = "C";
			// 
			// dToolStripMenuItem
			// 
			this.dToolStripMenuItem.Name = "dToolStripMenuItem";
			this.dToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.dToolStripMenuItem.Text = "D";
			// 
			// aAToolStripMenuItem
			// 
			this.aAToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
									this.aAAToolStripMenuItem});
			this.aAToolStripMenuItem.Name = "aAToolStripMenuItem";
			this.aAToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.aAToolStripMenuItem.Text = "AA";
			// 
			// aBToolStripMenuItem
			// 
			this.aBToolStripMenuItem.Name = "aBToolStripMenuItem";
			this.aBToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.aBToolStripMenuItem.Text = "AB";
			// 
			// aCToolStripMenuItem
			// 
			this.aCToolStripMenuItem.Name = "aCToolStripMenuItem";
			this.aCToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.aCToolStripMenuItem.Text = "AC";
			// 
			// aAAToolStripMenuItem
			// 
			this.aAAToolStripMenuItem.Name = "aAAToolStripMenuItem";
			this.aAAToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
			this.aAAToolStripMenuItem.Text = "AAA";
			// 
			// toolStripSeparator1
			// 
			this.toolStripSeparator1.Name = "toolStripSeparator1";
			this.toolStripSeparator1.Size = new System.Drawing.Size(149, 6);
			// 
			// MainForm
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(292, 273);
			this.Controls.Add(this.tvTest);
			this.Name = "MainForm";
			this.Text = "treeview";
			this.contextMenuStrip1.ResumeLayout(false);
			this.ResumeLayout(false);
		}
		private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
		private System.Windows.Forms.ToolStripMenuItem dToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem cToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem bToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem aCToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem aBToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem aAAToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem aAToolStripMenuItem;
		private System.Windows.Forms.ToolStripMenuItem aToolStripMenuItem;
		private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
		private System.Windows.Forms.TreeView tvTest;
	}
}
